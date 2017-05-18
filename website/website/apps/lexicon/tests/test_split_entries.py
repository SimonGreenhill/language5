from django.test import TestCase

from django.contrib.auth.models import User
from website.apps.core.models import Source, Language
from website.apps.lexicon.models import Word, Lexicon

from website.apps.lexicon.management.commands import split_entries

from website.apps.lexicon.tests.test_hygiene import HygieneDataMixin

class Test_Split_Entries(HygieneDataMixin):
    """Tests the split_entries management command"""
    def test_find_slash(self):
        cmd = split_entries.Command()
        assert self.slash in cmd.find_combined()

    def test_find_comma(self):
        cmd = split_entries.Command()
        assert self.comma in cmd.find_combined()

    def test_fail_on_zero_length_component_slash(self):
        """Test split_and_replace fails with a zero length component"""
        cmd = split_entries.Command()
        o = Lexicon.objects.create(
            language=self.lang,
            word=self.word,
            source=self.source,
            editor=self.editor,
            entry="/hello"
        )
        with self.assertRaises(AssertionError):
            cmd.split_and_replace(o, quiet=True)

    def test_fail_on_zero_length_component_comma(self):
        """Test split_and_replace fails with a zero length component"""
        cmd = split_entries.Command()
        o = Lexicon.objects.create(
            language=self.lang,
            word=self.word,
            source=self.source,
            editor=self.editor,
            entry=",hello"
        )
        with self.assertRaises(AssertionError):
            cmd.split_and_replace(o, quiet=True)

    def test_fail_on_zero_length_component_trailing_slash(self):
        """Test split_and_replace fails with a zero length component"""
        cmd = split_entries.Command()
        o = Lexicon.objects.create(
            language=self.lang,
            word=self.word,
            source=self.source,
            editor=self.editor,
            entry="hello/"
        )
        with self.assertRaises(AssertionError):
            cmd.split_and_replace(o, quiet=True)

    def test_fail_on_zero_length_component_trailing_comma(self):
        """Test split_and_replace fails with a zero length component"""
        cmd = split_entries.Command()
        o = Lexicon.objects.create(
            language=self.lang,
            word=self.word,
            source=self.source,
            editor=self.editor,
            entry="hello,"
        )
        with self.assertRaises(AssertionError):
            cmd.split_and_replace(o, quiet=True)

    def test_split_and_replace_slash(self):
        cmd = split_entries.Command()
        cmd.split_and_replace(self.slash, quiet=True)
        one = Lexicon.objects.filter(entry="hello")
        two = Lexicon.objects.filter(entry="world")

        assert len(one) == len(two) == 1
        one, two = one[0], two[0]

        assert one.language == two.language == self.slash.language
        assert one.editor == two.editor == self.slash.editor
        assert one.source == two.source == self.slash.source
        assert one.word == two.word == self.slash.word

    def test_split_and_replace_comma(self):
        cmd = split_entries.Command()
        cmd.split_and_replace(self.comma, quiet=True)
        one = Lexicon.objects.filter(entry="foo")
        two = Lexicon.objects.filter(entry="bar")

        assert len(one) == len(two) == 1
        one, two = one[0], two[0]

        assert one.language == two.language == self.comma.language
        assert one.editor == two.editor == self.comma.editor
        assert one.source == two.source == self.comma.source
        assert one.word == two.word == self.comma.word

    def test_split_and_replace_slash_deletes(self):
        cmd = split_entries.Command()
        # for some reason postgresql isn't setting slash/comman in setupTestData with a pk, this causes
        # problems when we work around it. So, requery the database to get the desired form.
        obj = Lexicon.objects.get(entry__contains="/")
        cmd.split_and_replace(obj, quiet=True)
        with self.assertRaises(Lexicon.DoesNotExist):
            assert Lexicon.objects.get(pk=self.slash.pk)

    def test_split_and_replace_comma_deletes(self):
        cmd = split_entries.Command()
        # for some reason postgresql isn't setting slash/comman in setupTestData with a pk, this causes
        # problems when we work around it. So, requery the database to get the desired form.
        obj = Lexicon.objects.get(entry__contains=",")
        cmd.split_and_replace(obj, quiet=True)
        with self.assertRaises(Lexicon.DoesNotExist):
            assert Lexicon.objects.get(pk=self.comma.pk)


    def test_split_and_replace_with_space(self):
        cmd = split_entries.Command()
        o = Lexicon.objects.create(
            language=self.lang,
            word=self.word,
            source=self.source,
            editor=self.editor,
            entry="i have/ a space"
        )
        cmd.split_and_replace(o, quiet=True)
        one = Lexicon.objects.filter(entry="i have")
        two = Lexicon.objects.filter(entry="a space")

        assert len(one) == len(two) == 1
        one, two = one[0], two[0]

        assert one.language == two.language == o.language
        assert one.editor == two.editor == o.editor
        assert one.source == two.source == o.source
        assert one.word == two.word == o.word


class Test_Filter(TestCase):
    """Tests the split_entries management command filtering"""
    @classmethod
    def setUpTestData(cls):
        cls.editor = User.objects.create(username='admin')
        cls.languages = [
            Language.objects.create(
                language='A', slug='a', isocode='aaa', editor=cls.editor
            ),
            Language.objects.create(
                language='B', slug='b', isocode='bbb', editor=cls.editor
            )
        ]
        cls.words = [
            Word.objects.create(word='hand', slug='hand', editor=cls.editor),
            Word.objects.create(word='leg', slug='leg', editor=cls.editor),
        ]
        cls.sources = [
            Source.objects.create(
                year=1992, author='Smith', slug='smith', editor=cls.editor
            ),
            Source.objects.create(
                year=1992, author='Jones', slug='jones', editor=cls.editor
            ),
        ]

        # make some items - each combination gets one combined entry
        # the _entry_ field is set to contain the language_id, word_id and
        # source_id
        for lang in cls.languages:
            for word in cls.words:
                for source in cls.sources:
                    Lexicon.objects.create(
                        language=lang,
                        word=word,
                        source=source,
                        editor=cls.editor,
                        entry="%d/%d/%d" % (lang.id, word.id, source.id)
                    )

    def _getvalues(self, obj):
        """
        Returns a dictionary of expected language_id, word_id, and source_id
        for this Lexical item.
        """
        return dict(zip(
            ['language', 'word', 'source'],
            [int(i) for i in obj.entry.split("/")]
        ))

    def test_find_all(self):
        """Tests whether we find all the combined entries."""
        assert len(split_entries.Command().find_combined()) == 8

    def test_filter_on_language(self):
        found = split_entries.Command().find_combined(
            language=self.languages[0]
        )
        assert len(found) == 4
        for f in found:
            values = self._getvalues(f)
            assert values['language'] == self.languages[0].id

    def test_filter_on_word(self):
        found = split_entries.Command().find_combined(word=self.words[0])
        assert len(found) == 4
        for f in found:
            values = self._getvalues(f)
            assert values['word'] == self.words[0].id

    def test_filter_on_source(self):
        found = split_entries.Command().find_combined(source=self.sources[0])
        assert len(found) == 4
        for f in found:
            values = self._getvalues(f)
            assert values['source'] == self.sources[0].id

    def test_filter_on_language_and_word(self):
        found = split_entries.Command().find_combined(
            language=self.languages[0],
            word=self.words[0]
        )
        assert len(found) == 2
        for f in found:
            values = self._getvalues(f)
            assert values['language'] == self.languages[0].id
            assert values['word'] == self.words[0].id

    def test_filter_on_language_and_word_and_source(self):
        found = split_entries.Command().find_combined(
            language=self.languages[0],
            word=self.words[0],
            source=self.sources[0]
        )
        assert len(found) == 1
        values = self._getvalues(found[0])
        assert values['language'] == self.languages[0].id
        assert values['word'] == self.words[0].id
        assert values['source'] == self.sources[0].id


class Test_Ignore_Protoforms(HygieneDataMixin):
    """Tests the split_entries management command ignores protoforms"""
    @classmethod
    def setUpTestData(cls):
        super(Test_Ignore_Protoforms, cls).setUpTestData()
        cls.pform1 = Lexicon.objects.create(
            language=cls.lang,
            word=cls.word,
            source=cls.source,
            editor=cls.editor,
            entry="*n(e,i)ri"
        )
        cls.pform2 = Lexicon.objects.create(
            language=cls.lang,
            word=cls.word,
            source=cls.source,
            editor=cls.editor,
            entry="*n(e/i)ri"
        )
        cls.pform3 = Lexicon.objects.create(
            language=cls.lang,
            word=cls.word,
            source=cls.source,
            editor=cls.editor,
            entry="*neri, *niri"
        )

    def test_comma(self):
        cmd = split_entries.Command()
        found = cmd.find_combined()
        assert self.pform1 not in found

    def test_slash(self):
        cmd = split_entries.Command()
        found = cmd.find_combined()
        assert self.pform2 not in found

    def test_correct(self):
        cmd = split_entries.Command()
        found = cmd.find_combined()
        # pform3 SHOULD be found
        assert self.pform3 in found

    def test_correctly_split_protoform(self):
        cmd = split_entries.Command()
        cmd.split_and_replace(self.pform3, quiet=True)
        one = Lexicon.objects.filter(entry="*neri")
        two = Lexicon.objects.filter(entry="*niri")

        assert len(one) == len(two) == 1
        one, two = one[0], two[0]

        assert one.language == two.language == self.pform3.language
        assert one.editor == two.editor == self.pform3.editor
        assert one.source == two.source == self.pform3.source
        assert one.word == two.word == self.pform3.word

