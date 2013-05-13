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
        