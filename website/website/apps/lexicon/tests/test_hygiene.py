from django.test import TestCase
from django.test.client import Client

from django.contrib.auth.models import User
from website.apps.core.models import Source, Language
from website.apps.lexicon.models import Word, Lexicon

from website.apps.lexicon.management.commands import hygiene


class HygieneDataMixin(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.editor = User.objects.create(username='admin')
        cls.word = Word.objects.create(
            word='Hand', slug='hand',
            full='a hand', editor=cls.editor
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
        
        # some ok entries;
        cls.good1 = Lexicon.objects.create(
            language=cls.lang,
            word=cls.word,
            source=cls.source,
            editor=cls.editor,
            entry="not empty"
        )
        cls.good2 = Lexicon.objects.create(
            language=cls.lang,
            word=cls.word,
            source=cls.source,
            editor=cls.editor,
            entry="a word"
        )
        
        cls.slash = Lexicon.objects.create(
            language=cls.lang,
            word=cls.word,
            source=cls.source,
            editor=cls.editor,
            entry="hello/world"
        )
        cls.comma = Lexicon.objects.create(
            language=cls.lang,
            word=cls.word,
            source=cls.source,
            editor=cls.editor,
            entry="foo, bar"
        )
        cls.dash = Lexicon.objects.create(
            language=cls.lang,
            word=cls.word,
            source=cls.source,
            editor=cls.editor,
            entry="-"
        )
        cls.dashdash = Lexicon.objects.create(
            language=cls.lang,
            word=cls.word,
            source=cls.source,
            editor=cls.editor,
            entry="--"
        )
        cls.dashdashdash =  Lexicon.objects.create(
            language=cls.lang,
            word=cls.word,
            source=cls.source,
            editor=cls.editor,
            entry="---"
        )
        cls.empty = Lexicon.objects.create(
            language=cls.lang,
            word=cls.word,
            source=cls.source,
            editor=cls.editor,
            entry=""
        )
        cls.count = Lexicon.objects.count()
        

class Test_Empty(HygieneDataMixin):
    """Tests the hygiene management command - find-empty"""
    def test_find_missing(self):
        cmd = hygiene.Command()
        assert self.empty in cmd.find_empty()

    def test_find_dash(self):
        cmd = hygiene.Command()
        assert self.dash in cmd.find_empty()

    def test_find_dashdash(self):
        cmd = hygiene.Command()
        assert self.dashdash in cmd.find_empty()

    def test_find_dashdashdash(self):
        cmd = hygiene.Command()
        assert self.dashdashdash in cmd.find_empty()

    def test_delete(self):
        cmd = hygiene.Command()
        cmd.delete(cmd.find_empty())
        assert Lexicon.objects.count() == self.count - 4, "Got : %d" % Lexicon.objects.count()


class Test_Duplicates(HygieneDataMixin):
    """Tests the hygiene management command - find-duplicates"""

    def test_find(self):
        dupe1 = Lexicon.objects.create(
            language=self.good1.language,
            word=self.good1.word,
            source=self.good1.source,
            editor=self.good1.editor,
            entry=self.good1.entry
        )
        cmd = hygiene.Command()
        dupes = cmd.find_duplicates()
        self.assertEqual(dupes, [dupe1])
    
    def test_delete(self):
        dupe1 = Lexicon.objects.create(
            language=self.good1.language,
            word=self.good1.word,
            source=self.good1.source,
            editor=self.good1.editor,
            entry=self.good1.entry
        )
        
        cmd = hygiene.Command()
        cmd.delete(cmd.find_duplicates())
        assert Lexicon.objects.count() == self.count, "Got: %d" % Lexicon.objects.count()

    def test_not_duplicate_if_different_word(self):
        newword = Word.objects.create(
            word='Banana', slug='banana', full='Yum', editor=self.editor
        )
        o = Lexicon.objects.create(
                language=self.good1.language,
                word=newword,
                source=self.good1.source,
                editor=self.good1.editor,
                entry=self.good1.entry
        )
        
        cmd = hygiene.Command()
        dupes = cmd.find_duplicates()
        assert len(dupes) == 0

    def test_not_duplicate_if_different_source(self):
        newsource = Source.objects.create(
            year=2013,
            author='Greenhill',
            slug='Greenhill2013',
            reference='...',
            comment='',
            editor=self.editor
        )
        o = Lexicon.objects.create(
            language=self.good1.language,
            word=self.good1.word,
            source=newsource,
            editor=self.good1.editor,
            entry=self.good1.entry
        )
        
        cmd = hygiene.Command()
        dupes = cmd.find_duplicates()
        assert len(dupes) == 0

    def test_not_duplicate_if_different_language(self):
        newlang = Language.objects.create(
            language='B',
            slug='langb',
            information='',
            classification='',
            isocode='bbb',
            editor=self.editor
        )
        o = Lexicon.objects.create(
            language=newlang,
            word=self.good1.word,
            source=self.good1.source,
            editor=self.good1.editor,
            entry=self.good1.entry
        )

        cmd = hygiene.Command()
        dupes = cmd.find_duplicates()
        assert len(dupes) == 0


class Test_FindUnstarred(HygieneDataMixin):
    """Tests the hygiene management command - find_unstarred"""
    def setUp(self):
        super(Test_FindUnstarred, self).setUp()
        self.ProtoLang = Language.objects.create(
            language="Proto-World",
            slug="proto-world",
            editor=self.editor
        )
        self.star = Lexicon.objects.create(
            language=self.ProtoLang,
            word=self.word,
            source=self.source,
            editor=self.editor,
            entry="*lima"
        )
        self.unstarred = Lexicon.objects.create(
            language=self.ProtoLang,
            word=self.word,
            source=self.source,
            editor=self.editor,
            entry="rima"
        )

    def test_find_unstarred(self):
        cmd = hygiene.Command()
        forms = cmd.find_unstarred()
        assert len(forms) == 1
        assert forms[0] == self.unstarred



