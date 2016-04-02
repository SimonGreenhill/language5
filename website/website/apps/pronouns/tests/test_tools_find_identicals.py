from django.test import TestCase

from website.apps.lexicon.models import Lexicon
from website.apps.pronouns.models import Paradigm
from website.apps.pronouns.tools import find_identicals

from website.apps.pronouns.tests import PronounsTestData


class TestFindIdenticals(PronounsTestData, TestCase):
    def test_ignore_empties(self):
        ident = find_identicals(self.pdm)
        assert len(ident) == 0
        
    def test_find_identicals(self):
        expected_pks = []
        pdm = Paradigm.objects.create(
            language=self.lang,
            source=self.source,
            editor=self.editor,
            comment="test_partial_prefill"
        )
        pdm._prefill_pronouns()
        
        for p in pdm.pronoun_set.all()[0:3]:
            p.entries.add(Lexicon.objects.create(
                editor=self.editor,
                source=self.source,
                language=self.lang,
                word=self.word,
                entry="fudge"
            ))
            p.save()
            expected_pks.append(p.id)
            
        ident = find_identicals(pdm)
        # right length?
        assert len(ident) == 3, "Expected 3, got: %r" % ident
        # right PKs found?
        seen_pks = set()
        for i, j in ident:
            assert i[0] in expected_pks
            assert j[0] in expected_pks
            seen_pks.add(i[0])
            seen_pks.add(j[0])

        # All PKs found?
        assert len(seen_pks) == 3
        for seen_pk in seen_pks:
            assert seen_pk in expected_pks

