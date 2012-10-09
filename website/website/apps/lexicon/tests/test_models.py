from django.contrib.auth.models import User
from django.test import TestCase

from website.apps.lexicon.models import Word, WordSubset, Lexeme, Cognate

class TestSetup(object):
    """Mixin for test data"""
    def setUp(self):
        self.editor = User.objects.create(username='admin')
        self.word1 = Word.objects.create(word='Hand', slug='hand', 
                                        full='a hand', editor=self.editor)
        self.word2 = Word.objects.create(word='One', slug='one', 
                                        full='1', editor=self.editor)
        self.word3 = Word.objects.create(word='Two', slug='two', 
                                        full='2', editor=self.editor)
        
        # subset "all" contains all three words
        self.subset_all = WordSubset.objects.create(subset='All words', 
                                        slug='all', description="Everthing", 
                                        editor=self.editor)
        self.subset_all.words.add(self.word1)
        self.subset_all.words.add(self.word2)
        self.subset_all.words.add(self.word3)
        
        # subset "numbers" contains words 2 and 3 but not 1
        self.subset_numbers = WordSubset.objects.create(subset='Numbers', 
                                        slug='numbers', description="For countin'", 
                                        editor=self.editor)
        self.subset_numbers.words.add(self.word2)
        self.subset_numbers.words.add(self.word3)
        
        # subset "nothing" contains nothing.
        self.subset_nothing = WordSubset.objects.create(subset='nothing', 
                                        slug='nothing', description="Nothing much", 
                                        editor=self.editor)

        
    def _compare_objects(self, original, saved):
        """Compares an `original` django model object to a `saved` version"""
        for field in original._meta.fields:
            self.assertEquals(getattr(original, field.name), getattr(saved, field.name))
        return True
    

class Test_Words(TestSetup, TestCase):
    """Simple tests for words"""
    def test_obj_one(self):
        """Simple test for object setting/retrieval"""
        self._compare_objects(self.word1, Word.objects.get(pk=1))
        
    def test_obj_two(self):
        """Simple test for object setting/retrieval"""
        self._compare_objects(self.word2, Word.objects.get(pk=2))
            
    def test_obj_three(self):
        """Simple test for object setting/retrieval"""
        self._compare_objects(self.word3, Word.objects.get(pk=3))
    
    
class Test_WordSubset(TestSetup, TestCase):
    """Tests for word subsets"""
    def test_obj_one(self):
        """Simple test for object setting/retrieval"""
        self._compare_objects(self.subset_all, WordSubset.objects.get(pk=self.subset_all.id))
        
    def test_obj_two(self):
        """Simple test for object setting/retrieval"""
        self._compare_objects(self.subset_numbers, WordSubset.objects.get(pk=self.subset_numbers.id))
        
    def test_obj_three(self):
        """Simple test for object setting/retrieval"""
        self._compare_objects(self.subset_nothing, WordSubset.objects.get(pk=self.subset_nothing.id))
        
    def test_subset_all(self):
        """Test that the set `all` is ok"""
        s = WordSubset.objects.get(slug="all")
        self.assertEquals(len(s.words.all()), 3)
    
    def test_subset_numbers(self):
        """Test that the set `numbers` is ok"""
        s = WordSubset.objects.get(slug="numbers")
        self.assertEquals(len(s.words.all()), 2)
        
    def test_subset_numbers(self):
        """Test that the set `nothing` is ok"""
        s = WordSubset.objects.get(slug="nothing")
        self.assertEquals(len(s.words.all()), 0)
    
    def test_get_all_sets_for_word(self):
        # word one is only in one set
        self.assertEquals(len(self.word1.wordsubset_set.all()), 1)
        self.assertEquals(self.word1.wordsubset_set.all()[0], self.subset_all)
        
        # word 2 is in sets all and numbers
        self.assertEquals(len(self.word2.wordsubset_set.all()), 2)
        self.assertEquals(self.word2.wordsubset_set.all()[0], self.subset_all)
        self.assertEquals(self.word2.wordsubset_set.all()[1], self.subset_numbers)
        

class Test_Lexeme(TestCase):
    def test(self):
        raise NotImplementedError("Not yet implemented.")

class Test_Cognate(TestCase):
    def test(self):
        raise NotImplementedError("Not yet implemented.")


