from django.test import TestCase

from website.apps.pronouns.models import Paradigm, Pronoun
from website.apps.pronouns.tools import extract_rule
from website.apps.pronouns.tests.test_views import DefaultSettingsMixin


class TestExtractRule(TestCase):
    
    def test_empty_fields_get_ignored(self):
        "Empty fields don't get processed"
        rules = extract_rule({
            'alignment_one': u'---',
            'alignment_two': u'---',
            'gender_one': u'---',
            'gender_two': u'---',
            'number_one': u'---',
            'number_two': u'---',
            'person_one': u'1',
            'person_two': u'12',
            'relationship': u'FO'
        })
        assert rules['one'].keys() == ['person']
        assert rules['two'].keys() == ['person']

    def test_error_on_no_relationship_value(self):
        "ValueError on no relationship value"
        with self.assertRaises(ValueError):
            rules = extract_rule({
                'person_one': u'1',
                'person_two': u'12',
            })
        
    def test_error_on_no_operand_one(self):
        "ValueError on no operand (i.e. nothing in rule[1] or rule[2])"
        with self.assertRaises(ValueError):
            rules = extract_rule({
                'person_two': u'12',
                'relationship': u'---'
            })
        
    def test_error_on_no_operand_two(self):
        "ValueError on no operand (i.e. nothing in rule[1] or rule[2])"
        with self.assertRaises(ValueError):
            rules = extract_rule({
                'person_one': u'12',
                'relationship': u'---'
            })
    
    def test_ignore_extra_fields(self):
        "Empty Ignore Irrelevant Fields"
        rules = extract_rule({
            'fudge_one': u'1',
            'fudge_two': u'2',
            'person_one': u'1',
            'person_two': u'12',
            'relationship': u'FO'
        })
        assert rules['one'].keys() == ['person']
        assert rules['two'].keys() == ['person']
