from __future__ import unicode_literals
from io import StringIO
from django.test import TestCase
from django.contrib.auth.models import User
from website.apps.lexicon.models import Word
from website.apps.entry.management.commands import create_wordlist

class TestWordlistParser(TestCase):
    """Tests the wordlist parser in the management comment"""
    @classmethod
    def setUpTestData(cls):
        # create a few words
        cls.editor = User.objects.create_user(
            'admin', 'admin@example.com', "test"
        )
        cls.word1 = Word.objects.create(editor=cls.editor, word="1", slug="one")
        cls.word2 = Word.objects.create(editor=cls.editor, word="2", slug="two")
        cls.cmd = create_wordlist.Command()
    
    def test_ignore_comment(self):
        content = StringIO()
        content.write('one\n')
        content.write('#comment\n')
        content.write('two\n')
        content.seek(0) # rewind
        wl = self.cmd.parse(content)
        assert len(wl) == 2
        assert wl[1] == self.word1
        assert wl[2] == self.word2
    
    def test_strips_whitespace(self):
        content = StringIO()
        content.write('one                                    \n')
        content.write('two\n')
        content.seek(0) # rewind
        wl = self.cmd.parse(content)
        assert len(wl) == 2
        assert wl[1] == self.word1
        assert wl[2] == self.word2
    
    def test_ignores_empty_lines(self):
        content = StringIO()
        content.write('one\n')
        content.write('\n')
        content.write('two\n')
        content.seek(0) # rewind
        wl = self.cmd.parse(content)
        assert len(wl) == 2
        assert wl[1] == self.word1
        assert wl[2] == self.word2
        
    def test_missing(self):
        content = StringIO()
        content.write('one\n')
        content.write('two\n')
        content.write('three\n')
        content.seek(0) # rewind
        with self.assertRaises(Word.DoesNotExist):
            wl = self.cmd.parse(content)
            
    def test_multiple_missing(self):
        content = StringIO()
        content.write('one\n')
        content.write('two\n')
        content.write('three\n')
        content.write('four\n')
        content.write('five\n')
        content.seek(0) # rewind
        with self.assertRaises(Word.DoesNotExist):
            wl = self.cmd.parse(content)

    def test_duplicate_word(self):
        content = StringIO()
        content.write('one\n')
        content.write('one\n')
        content.write('two\n')
        content.seek(0) # rewind
        wl = self.cmd.parse(content)
        assert len(wl) == 3
        assert wl[1] == self.word1
        assert wl[2] == self.word1
        assert wl[3] == self.word2
        
    def test_number_and_word(self):
        content = StringIO()
        content.write('1 one\n')
        content.write('2 two\n')
        content.seek(0) # rewind
        wl = self.cmd.parse(content)
        assert len(wl) == 2
        assert wl[1] == self.word1
        assert wl[2] == self.word2
        
    def test_number_and_word_ordering(self):
        content = StringIO()
        content.write('2 one\n')
        content.write('1 two\n')
        content.seek(0) # rewind
        wl = self.cmd.parse(content)
        assert len(wl) == 2
        assert wl[1] == self.word2
        assert wl[2] == self.word1
        
    def test_error_on_space(self):
        content = StringIO()
        content.write('a one\n')
        content.write('b two\n')
        content.seek(0) # rewind
        with self.assertRaises(ValueError):
            wl = self.cmd.parse(content)
    
    def test_create(self):
        content = StringIO()
        content.write('one\n')
        content.write('two\n')
        content.write('three\n')
        content.seek(0) # rewind
        
        assert Word.objects.count() == 2
        wl = self.cmd.parse(content, create=True)
        assert Word.objects.count() == 3
        assert Word.objects.get(slug='three')