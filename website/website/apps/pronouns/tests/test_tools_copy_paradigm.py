from django.test import TestCase

from website.apps.core.models import Language
from website.apps.pronouns.models import Paradigm, Pronoun
from website.apps.pronouns.tools import copy_paradigm
from website.apps.pronouns.tests.test_views import DefaultSettingsMixin


class TestCopyParadigm(DefaultSettingsMixin, TestCase):

    def setUp(self):
        self.add_fixtures()
                                    
    def test_adds_paradigm(self):
        pass
    
    def test_adds_rules(self):
        pass
        
    def test_adds_relationships(self):
        pass
    
    def test_adds_pronouns(self):
        pass