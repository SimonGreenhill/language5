from django.test import TestCase
from django.test.client import Client

from django.contrib.auth.models import User
from website.apps.core.models import Source, Language
from website.apps.lexicon.models import Word, Lexicon

from website.apps.lexicon.management.commands import mergeword


class TestMergeWordManagementCommand(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.editor = User.objects.create(username='admin')
        cls.word1 = Word.objects.create(
            word='Hand', slug='hand',
            full='a hand', editor=cls.editor
        )
        cls.word2 = Word.objects.create(
            word='Leg', slug='leg',
            full='a leg', editor=cls.editor
        )
        cls.lang = Language.objects.create(
            language='A', slug='lang',
            information='i.1', classification='a, b',
            isocode='aaa', editor=cls.editor
        )
        cls.source = Source.objects.create(
            year="1991", author='Smith',
            slug='Smith1991', reference='S2',
            comment='c1', editor=cls.editor
        )
        cls.lex_1_1 = Lexicon.objects.create(
            language=cls.lang,
            word=cls.word1,
            source=cls.source,
            editor=cls.editor,
            entry="1_1"
        )
        cls.lex_1_2 = Lexicon.objects.create(
            language=cls.lang,
            word=cls.word1,
            source=cls.source,
            editor=cls.editor,
            entry="1_2"
        )
        cls.lex_2_1 = Lexicon.objects.create(
            language=cls.lang,
            word=cls.word2,
            source=cls.source,
            editor=cls.editor,
            entry="2_1"
        )
        cls.lex_2_2 = Lexicon.objects.create(
            language=cls.lang,
            word=cls.word2,
            source=cls.source,
            editor=cls.editor,
            entry="2_2"
        )

    def test_error_on_invalid_args(self):
        cmd = mergeword.Command()
        with self.assertRaises(IndexError):
            cmd.handle(quiet=True)
        with self.assertRaises(IndexError):
            cmd.handle('hand', quiet=True)
        with self.assertRaises(IndexError):
            cmd.handle('hand', 'leg', 'foot', quiet=True)

    def test_error_on_bad_slug_arg1(self):
        cmd = mergeword.Command()
        with self.assertRaises(Word.DoesNotExist):
            cmd.handle('foot', 'hand', quiet=True)

    def test_error_on_bad_slug_arg2(self):
        cmd = mergeword.Command()
        with self.assertRaises(Word.DoesNotExist):
            cmd.handle('hand', 'nose', quiet=True)

    def test_does_nothing_without_save_option(self):
        cmd = mergeword.Command()
        cmd.handle('hand', 'leg', quiet=True)
        assert Lexicon.objects.get(pk=self.lex_2_1.pk).word == self.word2
        assert Lexicon.objects.get(pk=self.lex_2_2.pk).word == self.word2

    def test_works(self):
        cmd = mergeword.Command()
        cmd.handle('hand', 'leg', save=True, quiet=True)
        assert Lexicon.objects.get(pk=self.lex_2_1.pk).word == self.word1
        assert Lexicon.objects.get(pk=self.lex_2_2.pk).word == self.word1

