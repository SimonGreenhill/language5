from reversion import revisions as reversion
from reversion.models import Version
from django.test import TestCase
from django.test.client import Client
from django.forms import ValidationError
from django.core.urlresolvers import reverse

from website.apps.cognacy.tests.data import DataMixin
from website.apps.lexicon.models import Lexicon, CognateSet, Cognate, CognateNote


class Test_Save(DataMixin):
    """Tests the Cognate Save View"""
    url = reverse('cognacy:save', kwargs={'word': 'hand', 'clade': ''})
    
    def setUp(self):
        super(Test_Save, self).setUp()
        self.AuthenticatedClient = Client()
        self.AuthenticatedClient.login(username="admin", password="test")
        self.form_data = {
            'word': self.word.id, 
            'submit': 'true',
        }
    
    def test_error_when_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             "/accounts/login/?next=%s" % self.url,
                             status_code=302, target_status_code=200)
        
    def test_get_fails(self):
        response = self.AuthenticatedClient.get(self.url)
        # should just bounce back to /cognacy with no form
        self.assertRedirects(response, reverse('cognacy:do_index'),
            status_code=302, target_status_code=200
        )
        
    def test_post_ok(self):
        response = self.AuthenticatedClient.post(self.url, self.form_data, follow=True)
        # should just bounce back to the do-cognacy url
        self.assertRedirects(response, 
            reverse('cognacy:do', kwargs={'word': 'hand', 'clade': ''}), 
            status_code=302, target_status_code=200
        )
    
    def test_invalid_c_xxx(self):
        form_data = self.form_data
        form_data['c-SAUSAGE'] = "hehehe"
        with self.assertRaises(ValueError):
            response = self.AuthenticatedClient.post(self.url, form_data, follow=True)
        
    def test_additions_to_existing_cognateset(self):
        lexica = self.cogset1.lexicon.all()
        assert len(lexica) == 1
        assert self.lex_a in lexica
        assert self.lex_b not in lexica
        assert self.lex_c not in lexica
        
        form_data = self.form_data
        form_data['c-%d' % self.lex_b.id] = "%s" % self.cogset1.id
        response = self.AuthenticatedClient.post(self.url, form_data, follow=True)
        
        lexica = self.cogset1.lexicon.all()
        assert len(lexica) == 2
        assert self.lex_a in lexica
        assert self.lex_b in lexica
        assert self.lex_c not in lexica
        
    def test_additions_to_new_cognateset(self):
        form_data = self.form_data
        form_data['c-%d' % self.lex_b.id] = "5"  # does not exist
        response = self.AuthenticatedClient.post(self.url, form_data, follow=True)
        assert CognateSet.objects.count() == 3
        newcog = CognateSet.objects.get(pk=5)
        lexica = newcog.lexicon.all()
        assert len(lexica) == 1
        assert self.lex_a not in lexica
        assert self.lex_b in lexica
            
    def test_deletions(self):
        Cognate.objects.create(
            lexicon=self.lex_b, cognateset=self.cogset1, editor=self.editor
        ).save()
        assert self.cogset2.lexicon.count() == 2
        form_data = self.form_data
        form_data['c-%d' % self.lex_a.id] = "-%d" % self.cogset1.id
        response = self.AuthenticatedClient.post(self.url, form_data, follow=True)
        lexica = self.cogset1.lexicon.all()
        assert len(lexica) == 1
        assert self.lex_a not in lexica
        assert self.lex_b in lexica
        assert Lexicon.objects.count() == 3  # haven't deleted the lexical items have we?
        
    def test_empty_cognate_set_removed(self):
        assert self.cogset1.lexicon.count() == 1
        pk = self.cogset1.pk
        form_data = self.form_data
        form_data['c-%d' % self.lex_a.id] = "-%d" % self.cogset1.id
        response = self.AuthenticatedClient.post(self.url, form_data, follow=True)
        with self.assertRaises(CognateSet.DoesNotExist):
            CognateSet.objects.get(pk=pk)
        
    def test_catch_non_numeric(self):
        form_data = self.form_data
        form_data['c-%d' % self.lex_a.id] = "banana"
        response = self.AuthenticatedClient.post(self.url, form_data, follow=True)
        assert b'ERROR &#39;banana&#39; for lexicon' in response.content
        
    def test_cant_be_in_same_set_twice(self):
        form_data = self.form_data
        form_data['c-%d' % self.lex_a.id] = "%s" % self.cogset1.id
        response = self.AuthenticatedClient.post(self.url, form_data, follow=True)
        lexica = self.cogset1.lexicon.all()
        assert len(lexica) == 1
    
    def test_creates_reversion(self):
        form_data = self.form_data
        form_data['c-%d' % self.lex_b.id] = "%s" % self.cogset1.id
        form_data['c-%d' % self.lex_a.id] = "-%s" % self.cogset1.id
        response = self.AuthenticatedClient.post(self.url, form_data, follow=True)
        
        version_list = Version.objects.get_for_object(self.cogset1)
        assert len(version_list) == 1, "Cognate Version List Missing"
        
        version_list = Version.objects.get_for_object(self.lex_b)
        assert len(version_list) == 1, "Lex B Version List Missing"
        
        assert len(Version.objects.get_deleted(Cognate)) == 1
    
    def test_commands_DELETE(self):
        assert len(Version.objects.get_deleted(Lexicon)) == 0
        assert Lexicon.objects.get(pk=self.lex_b.id)  # exists?
        form_data = self.form_data
        form_data['c-%d' % self.lex_b.id] = "!DELETE"
        response = self.AuthenticatedClient.post(self.url, form_data, follow=True)
        with self.assertRaises(Lexicon.DoesNotExist):
            Lexicon.objects.get(pk=self.lex_b.id)
    
    def test_notes(self):
        form_data = self.form_data
        form_data['comment-word'] = self.word.id
        form_data['comment-comment'] = "this is a test"
        response = self.AuthenticatedClient.post(self.url, form_data, follow=True)
        assert CognateNote.objects.all().filter(word=self.word)[0].note == "this is a test"
 