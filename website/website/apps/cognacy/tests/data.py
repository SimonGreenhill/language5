from django.test import TestCase
from django.test.client import Client

from django.contrib.auth.models import User
from website.apps.core.models import Language, Source
from website.apps.lexicon.models import Word, Lexicon, CognateSet, Cognate, CognateNote

class DataMixin(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.editor = User.objects.create_user(
            'admin', 'admin@example.com', 'test'
        )
        cls.source = Source.objects.create(
            year="1991", author='Greenhill', 
            slug='greenhill1991', reference='',
            comment='', editor=cls.editor
        )
        cls.lang_a = Language.objects.create(
            language='A', slug='langa', 
            information='i.1', classification='a, a',
            isocode='aaa', editor=cls.editor
        )
        cls.lang_b = Language.objects.create(
            language='B', slug='langb', 
            information='i.1', classification='a, b',
            isocode='bbb', editor=cls.editor
        )
        cls.word = Word.objects.create(
            word='Hand', slug='hand', 
            full='a hand', editor=cls.editor
        )
        cls.lex_a = Lexicon.objects.create(
            language=cls.lang_a, 
            word=cls.word,
            source=cls.source,
            editor=cls.editor,
            entry='one'
        )
        cls.lex_b = Lexicon.objects.create(
            language=cls.lang_b, 
            word=cls.word,
            source=cls.source,
            editor=cls.editor,
            entry='two'
        )
        cls.lex_c = Lexicon.objects.create(
            language=cls.lang_b, 
            word=cls.word,
            source=cls.source,
            editor=cls.editor,
            entry='three'
        )
        # cognate sets
        cls.cogset1 = CognateSet.objects.create(
            protoform = "*t*",
            gloss = "starts with t",
            editor=cls.editor
        )
        cls.cogset2 = CognateSet.objects.create(
            protoform = "*o???",
            gloss = "starts with o",
            editor=cls.editor
        )
        # cognates
        cls.cog_1_a = Cognate.objects.create(
            lexicon=cls.lex_a, cognateset=cls.cogset1,
            source=cls.source,
            editor=cls.editor
        )
        cls.cog_2_b = Cognate.objects.create(
            lexicon=cls.lex_b, cognateset=cls.cogset2,
            source=cls.source,
            editor=cls.editor
        )
        # note: no source on this cognate
        cls.cog_2_c = Cognate.objects.create(
            lexicon=cls.lex_c, cognateset=cls.cogset2,
            editor=cls.editor
        )
        
