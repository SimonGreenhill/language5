from django.contrib.auth.models import User
from django.test import TestCase
from website.apps.core.tests.test_models import GenericCRUDTestMixin
from website.apps.core.tests.test_models import GenericCRUDTestMixinWithLanguage
from website.apps.core.tests.test_models import GenericCRUDTestMixinWithSource

from website.apps.lexicon.models import Word, WordSubset, Lexeme, Cognate

class Test_Word(GenericCRUDTestMixin, TestCase):
    """Tests the Word Model"""
    vars = {
        'word': 'Hand',
        'slug': 'hand',
        'full': 'a body part',
    }
    model = Word

    
class Test_WordSubset(TestCase):
    def setUp(self):
        self.editor = User.objects.create(username='admin')
        self.word1 = Word.objects.create(word='Hand', slug='hand', 
                                        full='a hand', editor=self.editor)
        self.word2 = Word.objects.create(word='One', slug='one', 
                                        full='1', editor=self.editor)
        self.word3 = Word.objects.create(word='Two', slug='two', 
                                        full='2', editor=self.editor)
    
    def test_subset(self):
        s = WordSubset.objects.create(subset='All words', slug='all', 
                                  description="Everthing", editor=self.editor)
        s.words.add(self.word1)
        s.words.add(self.word2)
        s.words.add(self.word3)
        s = WordSubset.objects.get(pk=s.id)
        
        self.assertEquals(len(s.words.all()), 3)
    
    def test_subset_numbers(self):
        s = WordSubset.objects.create(subset='Numbers', slug='numbers', 
                                  description="For countin'", editor=self.editor)
        s.words.add(self.word2)
        s.words.add(self.word3)
        s = WordSubset.objects.get(pk=s.id)
        self.assertEquals(len(s.words.all()), 2)



