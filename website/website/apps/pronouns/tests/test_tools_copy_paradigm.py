from django.test import TestCase

from website.apps.core.models import Language
from website.apps.pronouns.models import Paradigm, Pronoun
from website.apps.pronouns.tools import copy_paradigm
from website.apps.pronouns.tests.test_views import DefaultSettingsMixin


class TestCopyParadigm(DefaultSettingsMixin, TestCase):

    def setUp(self):
        self.add_fixtures()
        self.pdm = Paradigm.objects.create(language=self.lang, 
                                    source=self.source, 
                                    editor=self.editor,
                                    comment="test")

