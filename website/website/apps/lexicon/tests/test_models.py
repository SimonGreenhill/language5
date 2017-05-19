# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.test import TestCase

from website.apps.core.models import Language, Source

from website.apps.lexicon.tests import DataMixin

from website.apps.lexicon.models import Word, WordSubset, Lexicon
from website.apps.lexicon.models import CognateSet, Cognate
from website.apps.lexicon.models import CorrespondenceSet, Correspondence

class Test_Words(DataMixin, TestCase):
    def test_repr(self):
        assert str(self.word1) == "Hand (a hand)"
        self.word1.full = ""
        assert str(self.word1) == "Hand"
        
        w = Word.objects.create(word='Test', slug='test', editor=self.editor)
        w.save()
        assert str(w) == "Test", "Got %s not u'Test'" % unicode(w)
        
        # test we're ok with None
        w = Word.objects.create(word='Test2', slug='test2', full=None, editor=self.editor)
        w.save()
        assert str(w) == "Test2", "Got %s not u'Test2'" % unicode(w)


class Test_Lexicon(DataMixin, TestCase):
    def test_unicode(self):
        entry = "Iñtërnâtiônàlizætiøn"
        Lexicon.objects.create(language=self.lang1,
            source=self.source1, word=self.word2, entry=entry, phon_entry=None,
            annotation="", loan=False, loan_source=None, editor=self.editor)
        o = Lexicon.objects.get(entry=entry)
