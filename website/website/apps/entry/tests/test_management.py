import cStringIO
from django.test import TestCase
from django.contrib.auth.models import User
from website.apps.lexicon.models import Word
from website.apps.entry.management.commands import create_wordlist

class TestWordlistParser(TestCase):
    """Tests the wordlist parser in the management comment"""
    def setUp(self):
        # create a few words
        self.editor = User.objects.create_user('admin',
                                               'admin@example.com', "test")
        self.word1 = Word.objects.create(editor=self.editor, word="1", slug="one")
        self.word2 = Word.objects.create(editor=self.editor, word="2", slug="two")
        self.cmd = create_wordlist.Command()
    
    def test_ignore_comment(self):
        content = cStringIO.StringIO()
        content.write('one\n')
        content.write('#comment\n')
        content.write('two\n')
        content.reset() # rewind
        wl = self.cmd.parse(content)
        assert len(wl) == 2
        assert wl[1] == self.word1
        assert wl[2] == self.word2
    
    def test_strips_whitespace(self):
        content = cStringIO.StringIO()
        content.write('one                                    \n')
        content.write('two\n')
        content.reset() # rewind
        wl = self.cmd.parse(content)
        assert len(wl) == 2
        assert wl[1] == self.word1
        assert wl[2] == self.word2
    
    def test_ignores_empty_lines(self):
        content = cStringIO.StringIO()
        content.write('one\n')
        content.write('\n')
        content.write('two\n')
        content.reset() # rewind
        wl = self.cmd.parse(content)
        assert len(wl) == 2
        assert wl[1] == self.word1
        assert wl[2] == self.word2
        
    def test_missing(self):
        content = cStringIO.StringIO()
        content.write('one\n')
        content.write('two\n')
        content.write('three\n')
        content.reset() # rewind
        with self.assertRaises(Word.DoesNotExist):
            wl = self.cmd.parse(content)
            
    def test_multiple_missing(self):
        content = cStringIO.StringIO()
        content.write('one\n')
        content.write('two\n')
        content.write('three\n')
        content.write('four\n')
        content.write('five\n')
        content.reset() # rewind
        with self.assertRaises(Word.DoesNotExist):
            wl = self.cmd.parse(content)

    def test_duplicate_word(self):
        content = cStringIO.StringIO()
        content.write('one\n')
        content.write('one\n')
        content.write('two\n')
        content.reset() # rewind
        wl = self.cmd.parse(content)
        assert len(wl) == 3
        assert wl[1] == self.word1
        assert wl[2] == self.word1
        assert wl[3] == self.word2
        
    def test_number_and_word(self):
        content = cStringIO.StringIO()
        content.write('1 one\n')
        content.write('2 two\n')
        content.reset() # rewind
        wl = self.cmd.parse(content)
        assert len(wl) == 2
        assert wl[1] == self.word1
        assert wl[2] == self.word2
        
    def test_number_and_word_ordering(self):
        content = cStringIO.StringIO()
        content.write('2 one\n')
        content.write('1 two\n')
        content.reset() # rewind
        wl = self.cmd.parse(content)
        assert len(wl) == 2
        assert wl[1] == self.word2
        assert wl[2] == self.word1
        
    def test_error_on_space(self):
        content = cStringIO.StringIO()
        content.write('a one\n')
        content.write('b two\n')
        content.reset() # rewind
        with self.assertRaises(ValueError):
            wl = self.cmd.parse(content)
