from django.test import TestCase
from django.test.client import Client

from django.contrib.auth.models import User
from website.apps.core.models import Source, Language
from website.apps.lexicon.models import Word, Lexicon

from website.apps.lexicon.management.commands import mergeword


class TestMergeWordManagementCommand(TestCase):
    def setUp(self):
        self.editor = User.objects.create(username='admin')
        self.word1 = Word.objects.create(word='Hand', slug='hand', 
                                        full='a hand', editor=self.editor)
        self.word2 = Word.objects.create(word='Leg', slug='leg', 
                                        full='a leg', editor=self.editor)
        self.lang = Language.objects.create(language='A', slug='lang', 
                                             information='i.1', classification='a, b',
                                             isocode='aaa', editor=self.editor)
        self.source = Source.objects.create(year="1991", author='Smith', 
                                 slug='Smith1991', reference='S2',
                                 comment='c1', editor=self.editor)
        
        self.lex_1_1 = Lexicon.objects.create(
            language=self.lang, 
            word=self.word1,
            source=self.source,
            editor=self.editor,
            entry="1_1"
        )
        self.lex_1_2 = Lexicon.objects.create(
            language=self.lang, 
            word=self.word1,
            source=self.source,
            editor=self.editor,
            entry="1_2"
        )
        self.lex_2_1 = Lexicon.objects.create(
            language=self.lang, 
            word=self.word2,
            source=self.source,
            editor=self.editor,
            entry="2_1"
        )
        self.lex_2_2 = Lexicon.objects.create(
            language=self.lang, 
            word=self.word2,
            source=self.source,
            editor=self.editor,
            entry="2_2"
        )
    
    def test_error_on_invalid_args(self):
        cmd = mergeword.Command()
        with self.assertRaises(IndexError):
            cmd.handle()
        with self.assertRaises(IndexError):
            cmd.handle('hand')
        with self.assertRaises(IndexError):
            cmd.handle('hand', 'leg', 'foot')
    
    def test_error_on_bad_slug_arg1(self):
        cmd = mergeword.Command()
        with self.assertRaises(Word.DoesNotExist):
            cmd.handle('foot', 'hand')
            
    def test_error_on_bad_slug_arg2(self):
        cmd = mergeword.Command()
        with self.assertRaises(Word.DoesNotExist):
            cmd.handle('hand', 'nose')
    
    def test_does_nothing_without_save_option(self):
        cmd = mergeword.Command()
        cmd.handle('hand', 'leg')
        assert Lexicon.objects.get(pk=self.lex_2_1.pk).word == self.word2
        assert Lexicon.objects.get(pk=self.lex_2_2.pk).word == self.word2
        
    def test_works(self):
        cmd = mergeword.Command()
        cmd.handle('hand', 'leg', save=True)
        assert Lexicon.objects.get(pk=self.lex_2_1.pk).word == self.word1
        assert Lexicon.objects.get(pk=self.lex_2_2.pk).word == self.word1
        
