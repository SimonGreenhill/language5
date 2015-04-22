from django.test import TestCase

from django.test import TestCase
from django.test.client import Client
from django.forms import ValidationError
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
from website.apps.core.models import Language, Source
from website.apps.lexicon.models import Word, Lexicon, CognateSet, Cognate

class DataMixin(TestCase):
    def setUp(self):
        self.client = Client()
        self.editor = User.objects.create_user(
            'admin', 'admin@example.com', 'test'
        )
        self.source = Source.objects.create(
            year="1991", author='Greenhill', 
            slug='greenhill1991', reference='',
            comment='', editor=self.editor
        )
        self.lang_a = Language.objects.create(
            language='A', slug='langa', 
            information='i.1', classification='a, a',
            isocode='aaa', editor=self.editor
        )
        self.lang_b = Language.objects.create(
            language='B', slug='langb', 
            information='i.1', classification='a, b',
            isocode='bbb', editor=self.editor
        )
        self.word = Word.objects.create(
            word='Hand', slug='hand', 
            full='a hand', editor=self.editor
        )
        self.lex_a = Lexicon.objects.create(
            language=self.lang_a, 
            word=self.word,
            source=self.source,
            editor=self.editor,
            entry='one'
        )
        self.lex_b = Lexicon.objects.create(
            language=self.lang_b, 
            word=self.word,
            source=self.source,
            editor=self.editor,
            entry='two'
        )
        
        

class Test_Index(DataMixin):
    """Tests the Cognate List View"""
    url = reverse('cognacy:index')
    
    def test_template_used(self):
        self.client.login(username="admin", password="test")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'cognacy/index.html')
    
    def test_error_when_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302) 
        self.assertRedirects(response, 
                             "/accounts/login/?next=%s" % self.url, 
                             status_code=302, target_status_code=200)
        
    def test_ok_when_logged_in(self):
        self.client.login(username="admin", password="test")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_context_has_form(self):
        self.client.login(username="admin", password="test")
        response = self.client.get(self.url)
        assert 'form' in response.context
        
    def test_post(self):
        expected_url = reverse('cognacy:do', kwargs={'word': self.word.slug, 'clade': ''})
        self.client.login(username="admin", password="test")
        form_data = { 'word': self.word.id, 'submit': 'true',}
        response = self.client.post(self.url, form_data, follow=True)
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200)


class Test_Do(DataMixin):
    """Tests the Cognate Do View"""
    url = reverse('cognacy:do', kwargs={'word': 'hand', 'clade': ''})
    
    def setUp(self):
        super(Test_Do, self).setUp()
        self.AuthenticatedClient = Client()
        self.AuthenticatedClient.login(username="admin", password="test")
        self.response = self.AuthenticatedClient.get(self.url)
        
    def test_error_when_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             "/accounts/login/?next=%s" % self.url,
                             status_code=302, target_status_code=200)
        
    def test_ok_when_logged_in(self):
        self.client.login(username="admin", password="test")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
     
    def test_template_used(self):
        response = self.AuthenticatedClient.get(self.url)
        self.assertTemplateUsed(response, 'cognacy/detail.html')
    
    def test_has_inplay(self):
        assert 'inplay' in self.response.context
    
    def test_has_next_cognate(self):
        assert 'next_cognates' in self.response.context
        assert self.response.context['next_cognates'] == range(2, 12)
    
    def test_has_lexicon(self):
        assert 'lexicon' in self.response.context

    def test_has_word(self):
        assert 'word' in self.response.context
        assert self.response.context['word'] == self.word
    
    def test_has_clade(self):
        assert 'clade' in self.response.context
        assert self.response.context['clade'] == u''
    
    def test_has_form(self):
        assert 'form' in self.response.context
    
    def test_clade_filtering(self):
        # No filter -- get both langa and langb
        url = reverse('cognacy:do', kwargs={'word': 'hand', 'clade': ''})
        response = self.AuthenticatedClient.get(url)
        assert self.lex_a in response.context['lexicon'].data.data
        assert self.lex_b in response.context['lexicon'].data.data
        
        # filter -- get both langa and langb
        url = reverse('cognacy:do', kwargs={'word': 'hand', 'clade': 'a'})
        response = self.AuthenticatedClient.get(url)
        assert self.lex_a in response.context['lexicon'].data.data
        assert self.lex_b in response.context['lexicon'].data.data
        
        # filter -- only get langa
        url = reverse('cognacy:do', kwargs={'word': 'hand', 'clade': 'a, a'})
        response = self.AuthenticatedClient.get(url)
        assert self.lex_a in response.context['lexicon'].data.data
        assert self.lex_b not in response.context['lexicon'].data.data
        
        # filter -- only get langb
        url = reverse('cognacy:do', kwargs={'word': 'hand', 'clade': 'a, b'})
        response = self.AuthenticatedClient.get(url)
        assert self.lex_a not in response.context['lexicon'].data.data
        assert self.lex_b in response.context['lexicon'].data.data
        
        # filter on nonexistent clade -- get nothing
        url = reverse('cognacy:do', kwargs={'word': 'hand', 'clade': 'x'})
        response = self.AuthenticatedClient.get(url)
        assert response.context['lexicon'].data.data == []
      


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
        self.cogset = CognateSet.objects.create(protoform='test', editor=self.editor)
        Cognate.objects.create(
            lexicon=self.lex_a, cognateset=self.cogset, editor=self.editor
        ).save()
    
    def test_error_when_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             "/accounts/login/?next=%s" % self.url,
                             status_code=302, target_status_code=200)
        
    def test_get_fails(self):
        response = self.AuthenticatedClient.get(self.url)
        # should just bounce back to /cognacy with no form
        self.assertRedirects(response, reverse('cognacy:index'),
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
        lexica = self.cogset.lexicon.all()
        assert len(lexica) == 1
        assert self.lex_a in lexica
        assert self.lex_b not in lexica
        
        form_data = self.form_data
        form_data['c-%d' % self.lex_b.id] = "%s" % self.cogset.id
        response = self.AuthenticatedClient.post(self.url, form_data, follow=True)
        
        lexica = self.cogset.lexicon.all()
        assert len(lexica) == 2
        assert self.lex_a in lexica
        assert self.lex_b in lexica
        
    def test_additions_to_new_cognateset(self):
        form_data = self.form_data
        form_data['c-%d' % self.lex_b.id] = "5"  # does not exist
        response = self.AuthenticatedClient.post(self.url, form_data, follow=True)
        assert CognateSet.objects.count() == 2
        newcog = CognateSet.objects.get(pk=5)
        lexica = newcog.lexicon.all()
        assert len(lexica) == 1
        assert self.lex_a not in lexica
        assert self.lex_b in lexica
            
    def test_deletions(self):
        Cognate.objects.create(
            lexicon=self.lex_b, cognateset=self.cogset, editor=self.editor
        ).save()
        assert self.cogset.lexicon.count() == 2
        form_data = self.form_data
        form_data['c-%d' % self.lex_a.id] = "-%d" % self.cogset.id
        response = self.AuthenticatedClient.post(self.url, form_data, follow=True)
        lexica = self.cogset.lexicon.all()
        assert len(lexica) == 1
        assert self.lex_a not in lexica
        assert self.lex_b in lexica
        
    def test_empty_cognate_set_removed(self):
        assert self.cogset.lexicon.count() == 1
        pk = self.cogset.pk
        form_data = self.form_data
        form_data['c-%d' % self.lex_a.id] = "-%d" % self.cogset.id
        response = self.AuthenticatedClient.post(self.url, form_data, follow=True)
        assert Cognate.objects.count() == 0
        with self.assertRaises(CognateSet.DoesNotExist):
            CognateSet.objects.get(pk=pk)
        
    def test_catch_non_numeric(self):
        form_data = self.form_data
        form_data['c-%d' % self.lex_a.id] = "banana"
        response = self.AuthenticatedClient.post(self.url, form_data, follow=True)
        assert 'ERROR u&#39;banana&#39; for lexicon 1 is not a number' in response.content
        
    def test_cant_be_in_same_set_twice(self):
        form_data = self.form_data
        form_data['c-%d' % self.lex_a.id] = "%s" % self.cogset.id
        response = self.AuthenticatedClient.post(self.url, form_data, follow=True)
        
        lexica = self.cogset.lexicon.all()
        assert len(lexica) == 1
    
    def test_creates_reversion(self):
        import reversion
        form_data = self.form_data
        form_data['c-%d' % self.lex_b.id] = "%s" % self.cogset.id
        form_data['c-%d' % self.lex_a.id] = "-%s" % self.cogset.id
        response = self.AuthenticatedClient.post(self.url, form_data, follow=True)
        
        version_list = reversion.get_for_object(self.lex_b)
        print version_list
        import IPython; IPython.embed()
        assert False
        