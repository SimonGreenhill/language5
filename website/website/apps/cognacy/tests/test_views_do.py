from django.test import TestCase
from django.test.client import Client
from django.forms import ValidationError
from django.core.urlresolvers import reverse

from website.apps.cognacy.tests.data import DataMixin
from website.apps.lexicon.models import CognateSet, Cognate, CognateNote
        

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
        self.assertTemplateUsed(response, 'cognacy/do_detail.html')
    
    def test_has_inplay(self):
        assert 'inplay' in self.response.context
    
    def test_has_next_cognate(self):
        assert 'next_cognates' in self.response.context
        assert self.response.context['next_cognates'] == range(3, 12 + 1)
        cogset = CognateSet.objects.create(protoform='test', editor=self.editor)
        response = self.AuthenticatedClient.get(self.url)
        assert response.context['next_cognates'] == range(4, 13 + 1)
        assert cogset.id not in response.context['next_cognates']
    
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
      
    def test_note_show_on_word(self):
        note = CognateNote.objects.create(word=self.word, editor=self.editor, note="WORD!")
        response = self.AuthenticatedClient.get(self.url)
        assert 'WORD!' in response.content
        
    def test_note_show_on_cogset(self):
        cogset = CognateSet.objects.create(protoform='test', editor=self.editor)
        Cognate.objects.create(lexicon=self.lex_a, cognateset=cogset, editor=self.editor)
        note = CognateNote.objects.create(cognateset=cogset, editor=self.editor, note="COGSET!")
        response = self.AuthenticatedClient.get(self.url)
        assert 'COGSET!' in response.content
        
        

