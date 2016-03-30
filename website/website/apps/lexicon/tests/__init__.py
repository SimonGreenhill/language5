# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from website.apps.core.models import Language, Source
from website.apps.lexicon.models import Word, WordSubset, Lexicon

class DataMixin(object):
    """Mixin for test data"""
    @classmethod
    def setUpTestData(cls):
        cls.editor = User.objects.create_user(
            'admin', 'admin@example.com', "test"
        )
        cls.word1 = Word.objects.create(
            word='Hand', slug='hand', full='a hand', editor=cls.editor
        )
        cls.word2 = Word.objects.create(
            word='One', slug='one', full='1', editor=cls.editor
        )
        cls.word3 = Word.objects.create(
            word='Two', slug='two', full='2', editor=cls.editor
        )
    
        # some languages
        cls.lang1 = Language.objects.create(
            language='A', slug='langa',
            information='i.1', classification='a, b',
            isocode='aaa', editor=cls.editor
        )
        cls.lang2 = Language.objects.create(
            language='B', slug='langb',
            information='i.2', classification='c, d, e',
            isocode='bbb', editor=cls.editor
        )

        # some sources
        cls.source1 = Source.objects.create(
            year="1991", author='Smith',
            slug='Smith1991', reference='S2',
            comment='c1', editor=cls.editor
        )
        cls.source2 = Source.objects.create(
            year=2002, author='Jones',
            slug='Jones2002', reference='J2',
            comment='c2', editor=cls.editor
        )

        # subset "all" contains all three words
        cls.subset_all = WordSubset.objects.create(
            subset='All words', slug='all',
            description="Everthing",
            editor=cls.editor
        )
        cls.subset_all.words.add(cls.word1)
        cls.subset_all.words.add(cls.word2)
        cls.subset_all.words.add(cls.word3)

        # subset "numbers" contains words 2 and 3 but not 1
        cls.subset_numbers = WordSubset.objects.create(
            subset='Numbers', slug='numbers',
            description="For countin'",
            editor=cls.editor
        )
        cls.subset_numbers.words.add(cls.word2)
        cls.subset_numbers.words.add(cls.word3)

        # subset "nothing" contains nothing.
        cls.subset_nothing = WordSubset.objects.create(
            subset='nothing', slug='nothing',
            description="Nothing much",
            editor=cls.editor
        )

        # 3 lexical items
        #   1 => language 1, word 1, source 1
        #   2 => language 2, word 2, source 2
        #   3 => language 1, word 2, source 1
        cls.lexicon1 = Lexicon.objects.create(
            language=cls.lang1,
            source=cls.source1,
            word=cls.word1,
            entry="A",
            phon_entry="a",
            annotation="",
            loan=False,
            loan_source=None,
            editor=cls.editor
        )
        cls.lexicon2 = Lexicon.objects.create(
            language=cls.lang2,
            source=cls.source2,
            word=cls.word2,
            entry="B",
            phon_entry="b",
            annotation="",
            loan=False,
            loan_source=None,
            editor=cls.editor
        )
        cls.lexicon3 = Lexicon.objects.create(
            language=cls.lang1,
            source=cls.source1,
            word=cls.word2,
            entry="C",
            phon_entry="c",
            annotation="",
            loan=False,
            loan_source=None,
            editor=cls.editor
        )

