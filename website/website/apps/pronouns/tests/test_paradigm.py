from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from website.apps.core.models import Language, Source
from website.apps.lexicon.models import Lexicon
from website.apps.pronouns.models import Paradigm, PronounType, Pronoun
from website.apps.pronouns.tools import full_repr_row

from website.apps.pronouns.tests import DefaultSettingsMixin


class Test_Paradigm(DefaultSettingsMixin, TestCase):
    def setUp(self):
        self.add_fixtures()
        
    def test_have_some_pronoun_types(self):
        assert self.pdm.pronoun_set.count() == 3
    
    def test_prefill(self):
        # make sure the correct number of pronouns is there..
        assert self.pdm.pronoun_set.count() == len(PronounType._generate_all_combinations())
        
        # check the pronouns themselves...
        for comb in PronounType._generate_all_combinations():
            queryset = Pronoun.objects.filter(pronountype=comb)
            assert len(queryset) == 1, 'Got {0} not one'.format(len(queryset))
        
        
    def test_partial_prefill(self):
        # we should have a full complement. 
        assert self.pdm.pronoun_set.count() == len(PronounType._generate_all_combinations())
        
        # Let's delete some...
        for pron in self.pdm.pronoun_set.all():
            if pron.pronountype.person == '2':
                pron.delete()
            else:
                # modify the stored entries so we can identify them later.
                pron.entries.add(Lexicon.objects.create(
                    editor=self.editor, 
                    source=self.source,
                    language=self.lang,
                    word=self.word,
                    entry="old"
                ))
                pron.save()
                
        # how many should we have deleted
        missing = [_ for _ in PronounType ._generate_all_combinations() if _.person == '2']
        assert len(missing) == 1
        assert self.pdm.pronoun_set.count() == (len(PronounType._generate_all_combinations()) - len(missing))
        
        # re-run prefill
        self.pdm._prefill_pronouns()
        
        # we should now have a full complement again.
        assert self.pdm.pronoun_set.count() == len(PronounType._generate_all_combinations())
        
        for pron in self.pdm.pronoun_set.all():
            if pron.pronountype.person == '2':
                assert pron.entries.count() == 0
            else:
                assert pron.entries.count() == 1
                assert pron.entries.all()[0].entry == 'old'
        
