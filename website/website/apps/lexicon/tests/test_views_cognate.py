from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from website.apps.lexicon.tests import DataMixin, DataMixinLexicon
from website.apps.lexicon.models import Word, WordSubset, Lexicon
from website.apps.lexicon.models import CognateSet, Cognate


class CognateSetMixin(object):
    """A mixin for cognate set information"""
    def add_cognates(self):
        self.lex1 = Lexicon.objects.create(
            language=self.lang1, 
            word=self.word1,
            source=self.source1,
            editor=self.editor,
            entry="sausage",
            annotation=""
        )
        self.lex2 = Lexicon.objects.create(
            language=self.lang1, 
            word=self.word1,
            source=self.source1,
            editor=self.editor,
            entry="wurst",
            annotation=""
        )
        self.lex3 = Lexicon.objects.create(
            language=self.lang1, 
            word=self.word1,
            source=self.source1,
            editor=self.editor,
            entry="banana",
            annotation=""
        )
        self.cogset1 = CognateSet.objects.create(
            protoform = "*sausage",
            gloss = "sausage-like things",
            editor=self.editor
        )
        
        Cognate.objects.create(lexicon=self.lex1, cognateset=self.cogset1, editor=self.editor)
        Cognate.objects.create(lexicon=self.lex2, cognateset=self.cogset1, editor=self.editor)
        
        self.cogset2 = CognateSet.objects.create(
            protoform = "*banana",
            gloss = "a delicious yellow fruit",
            editor=self.editor
        )
        Cognate.objects.create(lexicon=self.lex3, cognateset=self.cogset2, editor=self.editor)
        
        

class Test_CognateSetIndex(DataMixin, CognateSetMixin, TestCase):
    def setUp(self):
        super(Test_CognateSetIndex, self).setUp()
        self.add_cognates()
        self.url = reverse('cognateset-index')
    
    def test_200ok_logged_in(self):
        self.client.login(username="admin", password="test")
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
    
    def test_error_on_notlogged_in(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=%s" % self.url, 
                                    status_code=302, target_status_code=200)
    
    def test_template(self):
        self.client.login(username="admin", password="test")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'lexicon/cognateset_index.html')
    
    def test_get_data(self):
        self.client.login(username="admin", password="test")
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        assert '*sausage' in response.content
        assert '*banana' in response.content
        

class Test_CognateSetDetail(DataMixin, CognateSetMixin, TestCase):
    def setUp(self):
        super(Test_CognateSetDetail, self).setUp()
        self.add_cognates()
        self.url = reverse('cognateset-detail', kwargs={'pk': self.cogset1.id})
    
    def test_200ok_logged_in(self):
        self.client.login(username="admin", password="test")
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
    
    def test_error_on_notlogged_in(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=%s" % self.url, 
                                    status_code=302, target_status_code=200)
    
    def test_get_missing(self):
        self.client.login(username="admin", password="test")
        response = self.client.get(reverse('cognateset-detail', kwargs={'pk': 5}))
        self.assertEquals(response.status_code, 404)
        
    def test_template(self):
        self.client.login(username="admin", password="test")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'lexicon/cognateset_detail.html')
    
    def test_get_data(self):
        self.client.login(username="admin", password="test")
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        assert 'sausage' in response.content
        assert 'wurst' in response.content
        assert 'banana' not in response.content