from django.test import TestCase

from website.apps.pronouns.models import Paradigm, Pronoun
from website.apps.pronouns.tools import full_repr_row
from website.apps.pronouns.tests.test_views import DefaultSettingsMixin

class TestReprRow(DefaultSettingsMixin, TestCase):
    
    def setUp(self):
        self.add_fixtures()
    
    def test_obj(self):
        p = Pronoun.objects.create(paradigm=self.pdm, editor=self.editor,
                            number='sg', alignment="A", person="1", gender=None)
        assert full_repr_row(p) == "1st (excl) Person Singular"
    
    def test_dict(self):
        d = {
             'number': ('sg', 'Singular'), 
             'alignment': ('A', 'A'), 
             'person': ('1', '1st (excl) Person'),
             'gender': None,
        }
        assert full_repr_row(d) == "1st (excl) Person Singular"
        
    def test_obj_no_gender(self):
        p = Pronoun.objects.create(paradigm=self.pdm, editor=self.editor,
                            number='sg', alignment="A", person="1", gender="M")
        assert full_repr_row(p) == "1st (excl) Person Singular Masculine"
        
    def test_dict_no_gender(self):
        d = {
             'number': ('sg', 'Singular'), 
             'alignment': ('A', 'A'), 
             'person': ('1', '1st (excl) Person'),
             'gender': ('M', 'Masculine'),
        }
        assert full_repr_row(d) == "1st (excl) Person Singular Masculine"
        
    def test_no_errors(self):
        for row in Pronoun._generate_all_combinations():
            full_repr_row(row)

