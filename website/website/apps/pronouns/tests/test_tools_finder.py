# -*- coding: utf-8 -*-
from django.test import TestCase

from website.apps.pronouns.tools import PronounFinder
from website.apps.pronouns.tools.finder import SCORE_IDENTITY, SCORE_EMPTY, SCORE_SUBSTRING, SCORE_SIMILARITY_THRESHOLD

class TestFinder(TestCase):
    
    def setUp(self):
        self.pf = PronounFinder()
        
    def test_identical(self):
        assert self.pf.compare('simon', 'simon') == SCORE_IDENTITY
        
    def test_substring_1(self):
        assert self.pf.compare('si', 'simon') == SCORE_SUBSTRING
    
    def test_substring_2(self):
        assert self.pf.compare('simon', 'si') == SCORE_SUBSTRING
        
    def test_empty_1(self):
        assert self.pf.compare('', 'simon') == SCORE_EMPTY
        
    def test_empty_2(self):
        assert self.pf.compare('simon', '') == SCORE_EMPTY
        
    def test_guess_1(self):
        # one char change so lev. distance = 1
        # divided by max length = 3
        # and then subtracted from 1
        # before multiplying by 0.6
        assert self.pf.compare('aaa', 'aab') == ((1 - (1.0 / 3.0)) * SCORE_SIMILARITY_THRESHOLD)
    
    def test_guess_2(self):
        # two char change so lev. distance = 2
        # divided by max length = 3
        # and then subtracted from 1
        # before multiplying by 0.6
        assert self.pf.compare('aaa', 'abb') == ((1 - (2.0 / 3.0)) * SCORE_SIMILARITY_THRESHOLD)
        
    def test_guess_different(self):
        # three char change so lev. distance = 3
        # divided by max length = 3
        # and then subtracted from 1
        # before multiplying by 0.6
        assert self.pf.compare('aaa', 'bbb') == ((1 - (3.0 / 3.0)) * SCORE_SIMILARITY_THRESHOLD)

    def test_handles_unicode(self):
        # 1 char change so lev. distance = 1
        # divided by max length = 2
        # and then subtracted from 1
        # before multiplying by 0.6
        assert self.pf.compare(u'ba', u'bá') == ((1 - (1.0 / 2.0)) * SCORE_SIMILARITY_THRESHOLD)
        