from django.test import TestCase
from django.test.client import Client

from django.contrib.auth.models import User
from website.apps.core.models import Language, Source
from website.apps.lexicon.models import Word, Lexicon, CognateSet, Cognate, CognateNote

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
        self.lex_c = Lexicon.objects.create(
            language=self.lang_b, 
            word=self.word,
            source=self.source,
            editor=self.editor,
            entry='three'
        )
        # cognate sets
        self.cogset1 = CognateSet.objects.create(
            protoform = "*t*",
            gloss = "starts with t",
            editor=self.editor
        )
        self.cogset2 = CognateSet.objects.create(
            protoform = "*o???",
            gloss = "starts with o",
            editor=self.editor
        )
        # cognates
        self.cog_1_a = Cognate.objects.create(
            lexicon=self.lex_a, cognateset=self.cogset1,
            source=self.source,
            editor=self.editor
        )
        
        
        self.cog_2_b = Cognate.objects.create(
            lexicon=self.lex_b, cognateset=self.cogset2,
            source=self.source,
            editor=self.editor
        )
        # note: no source on this cognate
        self.cog_2_c = Cognate.objects.create(
            lexicon=self.lex_c, cognateset=self.cogset2,
            editor=self.editor
        )
        
