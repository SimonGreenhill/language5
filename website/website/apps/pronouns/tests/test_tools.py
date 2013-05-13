from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from website.apps.core.models import Language, Source
from website.apps.pronouns.models import Paradigm, Pronoun
from website.apps.pronouns.tools import repr_row, find_identicals

from website.apps.pronouns.tests.test_views import DefaultSettingsMixin

class Test_Tools_repr_row(DefaultSettingsMixin, TestCase):
    
    def setUp(self):
        self.add_fixtures()
        self.pdm = Paradigm.objects.create(language=self.lang, 
                                    source=self.source, 
                                    editor=self.editor,
                                    comment="test")
    
    def test_obj(self):
        p = Pronoun.objects.create(paradigm=self.pdm, editor=self.editor,
                            number='sg', alignment="A", person="1", gender=None)
        assert repr_row(p) == "1st (excl) Person Singular"
    
    def test_dict(self):
        d = {
             'number': ('sg', 'Singular'), 
             'alignment': ('A', 'A'), 
             'person': ('1', '1st (excl) Person'),
             'gender': None,
        }
        assert repr_row(d) == "1st (excl) Person Singular"
        
    def test_obj_no_gender(self):
        p = Pronoun.objects.create(paradigm=self.pdm, editor=self.editor,
                            number='sg', alignment="A", person="1", gender="M")
        assert repr_row(p) == "1st (excl) Person Singular Masculine"
        
    def test_dict_no_gender(self):
        d = {
             'number': ('sg', 'Singular'), 
             'alignment': ('A', 'A'), 
             'person': ('1', '1st (excl) Person'),
             'gender': ('M', 'Masculine'),
        }
        assert repr_row(d) == "1st (excl) Person Singular Masculine"
        
    def test_no_errors(self):
        for row in Pronoun._generate_all_combinations():
            repr_row(row)



class Test_Tools_find_identicals(DefaultSettingsMixin, TestCase):

    def setUp(self):
        self.add_fixtures()
        self.pdm = Paradigm.objects.create(language=self.lang, 
                                    source=self.source, 
                                    editor=self.editor,
                                    comment="test")
        
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