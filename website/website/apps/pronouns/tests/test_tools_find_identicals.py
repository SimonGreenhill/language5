from django.test import TestCase

from website.apps.pronouns.models import Paradigm, Pronoun
from website.apps.pronouns.tools import find_identicals

from website.apps.pronouns.tests import DefaultSettingsMixin


class TestFindIdenticals(DefaultSettingsMixin, TestCase):

    def setUp(self):
        self.add_fixtures()
        
    def test_ignore_empties(self):
        ident = find_identicals(self.pdm.pronoun_set.all())
        assert len(ident) == 0
        
    def test_ignore_self(self):
        p = self.pdm.pronoun_set.all()[0]
        p.form = 'foo'
        p.save()
        ident = find_identicals(self.pdm.pronoun_set.all())
        assert len(ident) == 0
        
    def test_find_identicals(self):
        expected_pks = []
        for p in self.pdm.pronoun_set.all()[0:3]:
            p.form = 'foo'
            p.save()
            expected_pks.append(p.id)
        
        ident = find_identicals(self.pdm.pronoun_set.all())
        # right length? 
        assert len(ident) == 3, "Expected 3, got: %r" % ident
        # right PKs found? 
        seen_pks = set()
        for i, j in ident:
            assert i.id in expected_pks
            assert j.id in expected_pks
            seen_pks.add(i.id)
            seen_pks.add(j.id)
        
        # All PKs found? 
        assert len(seen_pks) == 3
        for seen_pk in seen_pks:
            assert seen_pk in expected_pks
            
