from django.test import TestCase

from website.apps.pronouns.models import PronounType, Pronoun
from website.apps.pronouns.tools import full_repr_row
from website.apps.pronouns.tests import PronounsTestData

class TestReprRow(PronounsTestData, TestCase):
    
    def test_obj(self):
        pt = PronounType(
            number='sg',
            alignment="A",
            person="1",
            gender=None,
            sequence=10,
            editor=self.editor,
            word=self.word
        )
        p = Pronoun(
            paradigm=self.pdm,
            editor=self.editor,
            pronountype=pt
        )
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
        pt = PronounType(
            number='sg',
            alignment="A",
            person="1",
            gender="M",
            sequence=11,
            editor=self.editor,
            word=self.word
        )
        p = Pronoun(
            paradigm=self.pdm, editor=self.editor, pronountype=pt
        )
        assert full_repr_row(p) == "1st (excl) Person Singular Gender 1"
        
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

