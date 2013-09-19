from django.test import TestCase

from website.apps.lexicon.models import Lexicon
from website.apps.pronouns.tools import full_repr_row
from website.apps.pronouns.models import Paradigm, PronounType, Pronoun
from website.apps.pronouns.tests import DefaultSettingsMixin
from website.apps.pronouns.forms import create_pronoun_formset

class TestFormsetCreator(DefaultSettingsMixin, TestCase):
    def setUp(self):
        self.add_fixtures()
        # add some entries and comments
        for pron in self.pdm.pronoun_set.all():
            # modify the stored entries so we can identify them later.
            pron.entries.add(Lexicon.objects.create(
                editor=self.editor, 
                source=self.source,
                language=self.lang,
                word=self.word,
                entry='pron-{0}'.format(pron.id),
                annotation='ann-{0}'.format(pron.id)
            ))
            pron.save()
    
    
    def test_create(self):
        self.form = create_pronoun_formset(self.pdm)
        assert False
                
    def test_create_with_post(self):
        assert False
        
    def test_save(self):
        assert False
        
    def test_save_with_post(self):
        assert False