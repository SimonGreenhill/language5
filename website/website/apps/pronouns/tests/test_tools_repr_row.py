from django.test import TestCase

from website.apps.pronouns.models import Paradigm, PronounType, Pronoun
from website.apps.pronouns.tools import full_repr_row
from website.apps.pronouns.tests import DefaultSettingsMixin

class TestReprRow(DefaultSettingsMixin, TestCase):
    
    def setUp(self):
        self.add_fixtures()
    
    def test_obj(self):
        pt = PronounType.objects.create(number='sg', alignment="A", person="1", sequence=10,
                                        gender=None, editor=self.editor, word=self.word)
        p = Pronoun.objects.create(paradigm=self.pdm, editor=self.editor, 
                            pronountype=pt)
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
        pt = PronounType.objects.create(number='sg', alignment="A", person="1", sequence=11,
                                        gender="M", editor=self.editor, word=self.word)
        p = Pronoun.objects.create(paradigm=self.pdm, editor=self.editor, pronountype=pt)
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
        for row in PronounType._generate_all_combinations():
            full_repr_row(row)

