from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from test_models import TestSetup
from website.apps.lexicon.models import Word, WordSubset

class Test_WordIndex(TestSetup, TestCase):
    """Tests the Word Index page"""
    def setUp(self):
        self.client = Client()
        self.url = reverse('word-index')
        super(Test_WordIndex, self).setUp()
        
    def test_get_all_words(self):
        # just getting the words index should get all words.
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        assert 'table' in response.context
        self.assertEquals(len(response.context['table'].rows), 3)
    
    def test_get_has_subsets(self):
        # page should have subsets listed
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.context['subsets']), 3)
        self.assertEquals(len(response.context['subsets']), len(WordSubset.objects.all()))
        
    def test_get_no_subset_context_is_none(self):
        # if there's no subset requested then the var `subset` will be None
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['subset'], None)
        
    def test_get_subset(self):
        # if a subset is requested...
        response = self.client.get(self.url, {'subset': 'numbers'})
        # ... then the var `subset` will be the same as the GET request
        self.assertEquals(response.context['subset'].slug, 'numbers')
        # ...and the number of words will change.
        assert 'table' in response.context
        self.assertEquals(len(response.context['table'].rows), 2)
        
    def test_get_empty_subset(self):
        # if a subset is requested...
        response = self.client.get(self.url, {'subset': 'nothing'})
        # ... then the var `subset` will be the same as the GET request
        self.assertEquals(response.context['subset'].slug, 'nothing')
        # ...and the number of words will change.
        assert 'table' in response.context
        self.assertEquals(len(response.context['table'].rows), 0)
        
    def test_invalid_subset_raises_404(self):
        response = self.client.get(self.url, {'subset': 'fudge'})
        self.assertEquals(response.status_code, 404)
        

class Test_WordDetail(TestSetup, TestCase):
    def test_get_all_words(self):
        url = reverse('word-detail', kwargs={'slug': self.word1.slug})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        assert 'table' in response.context
        self.assertEquals(len(response.context['table'].rows), 1)
        
    def test_get_all_words_two(self):
        url = reverse('word-detail', kwargs={'slug': self.word2.slug})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        assert 'table' in response.context
        self.assertEquals(len(response.context['table'].rows), 2)
