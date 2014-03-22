# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from website.apps.core.models import Language, Source
from website.apps.lexicon.models import Word, WordSubset, Lexicon
from website.apps.lexicon.models import CognateSet, Cognate
from website.apps.lexicon.models import CorrespondenceSet, Correspondence

class DataMixin(object):
    """Mixin for test data"""
    def setUp(self):
        self.editor = User.objects.create_user('admin',
                                               'admin@example.com', "test")
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
        self.source1 = Source.objects.create(year="1991", author='Smith', 
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
                                        

class DataMixinLexicon(DataMixin):
    def setUp(self):
        super(DataMixinLexicon, self).setUp()
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
        
