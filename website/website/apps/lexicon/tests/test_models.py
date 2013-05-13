# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.test import TestCase
from django.db import IntegrityError

from website.apps.core.models import Language, Source

from website.apps.lexicon.models import Word, WordSubset, Lexicon
from website.apps.lexicon.models import CognateSet, Cognate
from website.apps.lexicon.models import CorrespondenceSet, Correspondence

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
        
        # some languages
        self.lang1 = Language.objects.create(language='A', slug='langa', 
                                             information='i.1', classification='a, b',
                                             isocode='aaa', editor=self.editor)
        self.lang2 = Language.objects.create(language='B', slug='langb',
                                             information='i.2', classification='c, d, e',
                                             isocode='bbb', editor=self.editor)
        
        # some sources
        self.source1 = Source.objects.create(year=1991, author='Smith', 
                                 slug='Smith1991', reference='S2',
                                 comment='c1', editor=self.editor)
        self.source2 = Source.objects.create(year=2002, author='Jones', 
                                 slug='Jones2002', reference='J2',
                                 comment='c2', editor=self.editor)
        
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
                                        
        # 3 lexical items
        #   1 => language 1, word 1, source 1
        #   2 => language 2, word 2, source 2
        #   3 => language 1, word 2, source 1
        self.lexicon1 = Lexicon.objects.create(language=self.lang1, 
            source=self.source1, word=self.word1, entry="A", phon_entry="a", 
            annotation="", loan=False, loan_source=None, editor=self.editor)
        self.lexicon2 = Lexicon.objects.create(language=self.lang2, 
            source=self.source2, word=self.word2, entry="B", phon_entry="b", 
            annotation="", loan=False, loan_source=None, editor=self.editor)
        self.lexicon3 = Lexicon.objects.create(language=self.lang1, 
            source=self.source1, word=self.word2, entry="C", phon_entry="c", 
            annotation="", loan=False, loan_source=None, editor=self.editor)


        
    def _compare_objects(self, original, saved):
        """Compares an `original` django model object to a `saved` version"""
        for field in original._meta.fields:
            if getattr(original, field.name) != getattr(saved, field.name):
                raise AssertionError("Expected %r for field %s got %r" % (getattr(original, field.name), field.name, getattr(saved, field.name)))
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
    
    def test_repr(self):
        assert unicode(self.word1) == u"Hand (a hand)"
        self.word1.full = ""
        assert unicode(self.word1) == u"Hand"
        
        w = Word.objects.create(word='Test', slug='test', editor=self.editor)
        w.save()
        assert unicode(w) == u"Test", "Got %s not u'Test'" % unicode(w)
        
        # test we're ok with None
        w = Word.objects.create(word='Test2', slug='test2', full=None, editor=self.editor)
        w.save()
        assert unicode(w) == u"Test2", "Got %s not u'Test2'" % unicode(w)
    
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
        
    def test_subset_nothing(self):
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
        

class Test_Lexicon(TestSetup, TestCase):
        
    def test_must_have_language(self):
        with self.assertRaises(ValueError):
            Lexicon.objects.create(language=None, 
                source=self.source2, word=self.word2, entry="Z", phon_entry="z", 
                annotation="", loan=False, loan_source=None, editor=self.editor)
        
    def test_must_have_source(self):
        with self.assertRaises(ValueError):
            Lexicon.objects.create(language=self.lang1, 
                source=None, word=self.word2, entry="Z", phon_entry="z", 
                annotation="", loan=False, loan_source=None, editor=self.editor)
    
    def test_must_have_word(self):
        with self.assertRaises(ValueError):
            Lexicon.objects.create(language=self.lang1, 
                source=self.source1, word=None, entry="Z", phon_entry="z", 
                annotation="", loan=False, loan_source=None, editor=self.editor)
    
    def test_must_have_entry(self):
        with self.assertRaises(IntegrityError):
            Lexicon.objects.create(language=self.lang1, 
                source=self.source1, word=self.word2, entry=None, phon_entry="z", 
                annotation="", loan=False, loan_source=None, editor=self.editor)
        
    def test_annotation_can_be_empty(self):
        Lexicon.objects.create(language=self.lang1, 
            source=self.source1, word=self.word2, entry="Z", phon_entry="z", 
            annotation=None, loan=False, loan_source=None, editor=self.editor)
        
    def test_phon_can_be_empty(self):
        Lexicon.objects.create(language=self.lang1, 
            source=self.source1, word=self.word2, entry="zz", phon_entry=None, 
            annotation="", loan=False, loan_source=None, editor=self.editor)
    
    def test_loan(self):
        Lexicon.objects.create(language=self.lang1, 
            source=self.source1, word=self.word2, entry="zz", phon_entry=None, 
            annotation="", loan=True, loan_source=self.lang1, editor=self.editor)
        
    def test_loan_with_no_source(self):
        Lexicon.objects.create(language=self.lang1, 
            source=self.source1, word=self.word2, entry="zz", phon_entry=None, 
            annotation="", loan=True, loan_source=None, editor=self.editor)
    
    def test_get_all_items_for_language(self):
        objs = self.lang1.lexicon_set.all().order_by('entry')
        self.assertEquals(len(objs), 2)
        self._compare_objects(objs[0], self.lexicon1)
        self._compare_objects(objs[1], self.lexicon3)
        
    def test_get_all_items_for_source(self):
        objs = self.source1.lexicon_set.all().order_by('entry')
        self.assertEquals(len(objs), 2)
        self._compare_objects(objs[0], self.lexicon1)
        self._compare_objects(objs[1], self.lexicon3)
        
    def test_get_all_items_for_word(self):
        objs = self.word2.lexicon_set.all().order_by('entry')
        self.assertEquals(len(objs), 2)
        self._compare_objects(objs[0], self.lexicon2)
        self._compare_objects(objs[1], self.lexicon3)
        
    def test_can_have_multiple_items_for_language_source_word(self):
        Lexicon.objects.create(language=self.lang1, 
            source=self.source1, word=self.word2, entry="V", phon_entry=None, 
            annotation="", loan=False, loan_source=None, editor=self.editor)
        Lexicon.objects.create(language=self.lang1, 
            source=self.source1, word=self.word2, entry="V", phon_entry=None, 
            annotation="", loan=False, loan_source=None, editor=self.editor)
        objs = Lexicon.objects.filter(language=self.lang1, source=self.source1, 
            word=self.word2, entry="V")
        self.assertEquals(len(objs), 2)
        
    def test_unicode(self):
        entry = u"Iñtërnâtiônàlizætiøn".encode('utf-8')
        Lexicon.objects.create(language=self.lang1, 
            source=self.source1, word=self.word2, entry=entry, phon_entry=None, 
            annotation="", loan=False, loan_source=None, editor=self.editor)
        o = Lexicon.objects.get(entry=entry)


class Test_CognateSet(TestSetup, TestCase):
    
    def test_create(self):
        CognateSet.objects.create(label="PPN *foo", source=self.source1, 
            comment="", quality=0, editor=self.editor)
    
    def test_label_can_be_empty(self):
        CognateSet.objects.create(label=None, source=self.source1, 
            comment="", quality=0, editor=self.editor)
        
    def test_source_can_be_empty(self):
        CognateSet.objects.create(label="PPN *foo", source=None, 
            comment="", quality=0, editor=self.editor)
        
    def test_comment_can_be_empty(self):
        CognateSet.objects.create(label="PPN *foo", source=self.source1, 
            comment=None, quality=0, editor=self.editor)
    
    def test_get_all_cognates_for_cognateset(self):
        cog = CognateSet.objects.create(label="PPN *foo", source=self.source1, 
            comment="", quality=0, editor=self.editor)
        c1 = Cognate.objects.create(lexicon=self.lexicon1, cognateset=cog, 
            source=self.source1, editor=self.editor)
        c2 = Cognate.objects.create(lexicon=self.lexicon2, cognateset=cog, 
            source=self.source1, editor=self.editor)
        
        assert c1 in cog.cognate_set.all()
        assert c2 in cog.cognate_set.all()
        assert len(cog.cognate_set.all()) == 2
        
    
class Test_Cognate(TestSetup, TestCase):
    
    def test_create(self):
        cog = CognateSet.objects.create(label="PPN *foo", source=self.source1, 
            comment="", quality=0, editor=self.editor)
        c1 = Cognate.objects.create(lexicon=self.lexicon1, cognateset=cog, 
            source=self.source1, editor=self.editor)
        c2 = Cognate.objects.create(lexicon=self.lexicon2, cognateset=cog, 
            source=self.source1, editor=self.editor)
        
    def test_source_can_be_empty(self):
        cog = CognateSet.objects.create(label="PPN *foo", source=self.source1, 
            comment="", quality=0, editor=self.editor)
        c1 = Cognate.objects.create(lexicon=self.lexicon1, cognateset=cog, 
            source=None, editor=self.editor)
        
    def test_comment_can_be_empty(self):
        cog = CognateSet.objects.create(label="PPN *foo", source=self.source1, 
            comment="", quality=0, editor=self.editor)
        c1 = Cognate.objects.create(lexicon=self.lexicon1, cognateset=cog, 
            source=self.source1, comment=None, editor=self.editor)
    

class Test_CorrespondenceSet(TestSetup, TestCase):
    def test_create(self):
        CorrespondenceSet.objects.create(source=self.source1, comment="", 
            editor=self.editor)
    
    def test_source_can_be_empty(self):
        CorrespondenceSet.objects.create(source=None, comment="", 
            editor=self.editor)
        
    def test_comment_can_be_empty(self):
        CorrespondenceSet.objects.create(source=self.source1, comment=None, 
            editor=self.editor)
    
    def test_get_all_correspondences_for_correspondenceset(self):
        corr = CorrespondenceSet.objects.create(source=self.source1, comment="", 
            editor=self.editor)
        
        # Wherever language 1 has a p, language 2 has an f (L1 p > L2 f)
        c1 = Correspondence.objects.create(language=self.lang1, corrset=corr, rule="p",
            editor=self.editor)
        c2 = Correspondence.objects.create(language=self.lang2, corrset=corr, rule="f",
            editor=self.editor)
            
        assert c1 in corr.correspondence_set.all()
        assert c2 in corr.correspondence_set.all()
        assert len(corr.correspondence_set.all()) == 2
        
    
class Test_Correspondence(TestSetup, TestCase):
    def test_create(self):
        corr = CorrespondenceSet.objects.create(source=self.source1, comment="", 
            editor=self.editor)
        Correspondence.objects.create(language=self.lang1, corrset=corr, rule="p",
            editor=self.editor)
    
    
    