from django.test import TestCase
from django.test.client import Client

from django.contrib.auth.models import User
from website.apps.core.models import Source, Language
from website.apps.lexicon.models import Word, Lexicon

from website.apps.lexicon.management.commands import split_entries

from test_hygiene import HygieneDataMixin

class Test_Split_Entries(HygieneDataMixin):
    """Tests the split_entries management command"""
    
    def setUp(self):
        super(Test_Split_Entries, self).setUp()
        
        self.combined = {
            'slash': Lexicon.objects.create(
                language=self.lang, 
                word=self.word,
                source=self.source,
                editor=self.editor,
                entry="hello/world"
            ),
            'comma': Lexicon.objects.create(
                language=self.lang, 
                word=self.word,
                source=self.source,
                editor=self.editor,
                entry="foo,bar"
            ),
        }
        
    def test_find_slash(self):
        cmd = split_entries.Command()
        assert self.combined['slash'] in cmd.find_combined()
    
    def test_find_comma(self):
        cmd = split_entries.Command()
        assert self.combined['comma'] in cmd.find_combined()
    
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
            cmd.split_and_replace(o)
        
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
            cmd.split_and_replace(o)
        
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
            cmd.split_and_replace(o)

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
            cmd.split_and_replace(o)
            
    def test_split_and_replace_slash(self):
        cmd = split_entries.Command()
        cmd.split_and_replace(self.combined['slash'])
        one = Lexicon.objects.filter(entry="hello")
        two = Lexicon.objects.filter(entry="world")
        
        assert len(one) == len(two) == 1
        one, two = one[0], two[0]
        
        assert one.language == two.language == self.combined['slash'].language
        assert one.editor == two.editor == self.combined['slash'].editor
        assert one.source == two.source == self.combined['slash'].source
        assert one.word == two.word == self.combined['slash'].word
        
    def test_split_and_replace_comma(self):
        cmd = split_entries.Command()
        cmd.split_and_replace(self.combined['comma'])
        one = Lexicon.objects.filter(entry="foo")
        two = Lexicon.objects.filter(entry="bar")
        
        assert len(one) == len(two) == 1
        one, two = one[0], two[0]
        
        assert one.language == two.language == self.combined['comma'].language
        assert one.editor == two.editor == self.combined['comma'].editor
        assert one.source == two.source == self.combined['comma'].source
        assert one.word == two.word == self.combined['comma'].word
    
    def test_split_and_replace_slash_deletes(self):
        cmd = split_entries.Command()
        cmd.split_and_replace(self.combined['slash'])
        with self.assertRaises(Lexicon.DoesNotExist):
            assert Lexicon.objects.get(pk=self.combined['slash'].pk)
        
    def test_split_and_replace_comma_deletes(self):
        cmd = split_entries.Command()
        cmd.split_and_replace(self.combined['comma'])
        with self.assertRaises(Lexicon.DoesNotExist):
            assert Lexicon.objects.get(pk=self.combined['comma'].pk)
        
    
    def test_split_and_replace_with_space(self):
        cmd = split_entries.Command()
        o = Lexicon.objects.create(
            language=self.lang, 
            word=self.word,
            source=self.source,
            editor=self.editor,
            entry="i have/ a space"
        ) 
        cmd.split_and_replace(o)
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

    def setUp(self):
        self.editor = User.objects.create(username='admin')
        self.languages = [
            Language.objects.create(
                language='A', slug='a', isocode='aaa', editor=self.editor),
            Language.objects.create(
                language='B', slug='b', isocode='bbb', editor=self.editor)
        ]
        self.words = [
            Word.objects.create(word='hand', slug='hand', editor=self.editor),
            Word.objects.create(word='leg', slug='leg', editor=self.editor),
        ]
        self.sources = [
            Source.objects.create(
                year=1992, author='Smith', slug='smith', editor=self.editor),
            Source.objects.create(
                year=1992, author='Jones', slug='jones', editor=self.editor),
        ]
        
        # make some items - each combination gets one combined entry
        # the _entry_ field is set to contain the language_id, word_id and source_id
        for lang in self.languages:
            for word in self.words:
                for source in self.sources:
                    Lexicon.objects.create(
                        language=lang, 
                        word=word,
                        source=source,
                        editor=self.editor,
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
        found = split_entries.Command().find_combined(language=self.languages[0])
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
        found = split_entries.Command().find_combined(language=self.languages[0], 
                                                      word=self.words[0])
        assert len(found) == 2
        for f in found:
            values = self._getvalues(f)
            assert values['language'] == self.languages[0].id
            assert values['word'] == self.words[0].id
    
    def test_filter_on_language_and_word_and_source(self):
        found = split_entries.Command().find_combined(language=self.languages[0], 
                                                      word=self.words[0],
                                                      source=self.sources[0])
        assert len(found) == 1
        values = self._getvalues(found[0])
        assert values['language'] == self.languages[0].id
        assert values['word'] == self.words[0].id
        assert values['source'] == self.sources[0].id
    