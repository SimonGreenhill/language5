from django.test import TestCase
from django.test.client import Client

from django.contrib.auth.models import User
from website.apps.core.models import Source, Language
from website.apps.lexicon.models import Word, Lexicon

from website.apps.lexicon.management.commands import write_table


class TestWriteTable(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cmd = write_table.Command()
        cls.editor = User.objects.create(username='admin')
        cls.word1 = Word.objects.create(
            word='Hand', slug='hand',
            full='a hand', editor=cls.editor
        )
        cls.word2 = Word.objects.create(
            word='Leg', slug='leg',
            full='a leg', editor=cls.editor
        )
        cls.lang1 = Language.objects.create(
            language='A', slug='lang_a',
            information='i.1', classification='a, x',
            isocode='aaa', editor=cls.editor
        )
        cls.lang2 = Language.objects.create(
            language='B', slug='lang_b',
            information='i.1', classification='b, x',
            isocode='bbb', editor=cls.editor
        )
        cls.source1 = Source.objects.create(
            year="1991", author='Smith',
            slug='Smith1991', reference='...',
            comment='', editor=cls.editor
        )
        cls.source2 = Source.objects.create(
            year="1992", author='Jones',
            slug='Jones1992', reference='...',
            comment='', editor=cls.editor
        )

        for word in [cls.word1, cls.word2]:
            for lang in [cls.lang1, cls.lang2]:
                for source in [cls.source1, cls.source2]:
                    Lexicon.objects.create(
                        language=lang,
                        word=word,
                        source=source,
                        editor=cls.editor,
                        entry="%s-%s-%s" % (word.slug, lang.slug, source.slug)
                    )

    def test_find_all(self):
        assert len(self.cmd.get_entries()) == Lexicon.objects.count()

    def test_filter_word(self):
        for lex in self.cmd.get_entries(word=self.word1.slug):
            assert lex.word == self.word1
        for lex in self.cmd.get_entries(word=self.word2.slug):
            assert lex.word == self.word2

    def test_filter_language(self):
        for lex in self.cmd.get_entries(language=self.lang1.slug):
            assert lex.language == self.lang1
        for lex in self.cmd.get_entries(language=self.lang2.slug):
            assert lex.language == self.lang2

    def test_filter_source(self):
        for lex in self.cmd.get_entries(source=self.source1.slug):
            assert lex.source == self.source1
        for lex in self.cmd.get_entries(source=self.source2.slug):
            assert lex.source == self.source2

    def test_filter_clade(self):
        for lex in self.cmd.get_entries(clade="a"):
            # should all belong to language 1
            assert lex.language == self.lang1
        for lex in self.cmd.get_entries(clade="b"):
            # should all belong to language 2
            assert lex.language == self.lang2

    def test_filter_language_source(self):
        for lex in self.cmd.get_entries(source=self.source1.slug, language=self.lang1.slug):
            assert lex.source == self.source1
            assert lex.language == self.lang1
        for lex in self.cmd.get_entries(source=self.source2.slug, language=self.lang1.slug):
            assert lex.source == self.source2
            assert lex.language == self.lang1

    def test_filter_word_source_language(self):
        for word in [self.word1, self.word2]:
            for lang in [self.lang1, self.lang2]:
                for source in [self.source1, self.source2]:
                    lex = self.cmd.get_entries(
                            source=source.slug, word=word.slug, language=lang.slug
                    )
                    assert len(lex) == 1
                    assert lex[0].entry == "%s-%s-%s" % (word.slug, lang.slug, source.slug)

