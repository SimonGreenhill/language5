from django.test import TestCase

from website.apps.core.models import Language
from website.apps.lexicon.models import Lexicon
from website.apps.pronouns.models import Paradigm, Pronoun, Rule, Relationship
from website.apps.pronouns.tools import copy_paradigm
from website.apps.pronouns.tests import PronounsTestData


class TestCopyParadigm(PronounsTestData, TestCase):
    
    @classmethod
    def setUpTestData(cls):
        super(TestCopyParadigm, cls).setUpTestData()
        cls.lang2 = Language.objects.create(
            language='B',
            slug='langb',
            information='',
            classification='',
            isocode='bbb',
            editor=cls.editor
        )
        cls.newpdm = copy_paradigm(cls.pdm, cls.lang2)
        
    def test_copies_paradigm_language(self):
        assert self.newpdm.language == self.lang2

    def test_copies_paradigm_source(self):
        assert self.newpdm.source == self.pdm.source

    def test_copies_paradigm_comment(self):
        assert self.newpdm.comment == self.pdm.comment

    def test_copies_paradigm_label(self):
        assert self.newpdm.label == self.pdm.label

    def test_copies_paradigm_analect(self):
        assert self.newpdm.analect == self.pdm.analect

    def test_adds_paradigm_doesnt_affect_previous(self):
        assert self.pdm.language == self.lang
        assert self.pdm.pk is not None
        assert Paradigm.objects.get(pk=self.pdm.pk) == self.pdm
        
    def test_adds_pronouns(self):
        old = {}
        for p in self.pdm.pronoun_set.all():
            old[p.pronountype] = sorted([e.entry for e in p.entries.all()])
        
        for new_p in self.newpdm.pronoun_set.all():
            entries = sorted([e.entry for e in new_p.entries.all()])
            self.assertEqual(old[new_p.pronountype], entries)
