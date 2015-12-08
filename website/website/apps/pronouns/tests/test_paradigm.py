from django.test import TestCase

from website.apps.lexicon.models import Lexicon
from website.apps.pronouns.models import PronounType, Pronoun

from website.apps.pronouns.tests import DefaultSettingsMixin


class Test_Paradigm(DefaultSettingsMixin, TestCase):
    def setUp(self):
        self.add_fixtures()
    
    def test_repr_no_label(self):
        assert unicode(self.pdm) == 'A'

    def test_repr_with_label(self):
        self.pdm.label = 'test'
        self.pdm.save()
        assert unicode(self.pdm) == 'A: test'
        
    def test_have_some_pronoun_types(self):
        assert self.pdm.pronoun_set.count() == 3
    
    def test_prefill(self):
        # make sure the correct number of pronouns is there..
        combs = PronounType._generate_all_combinations()
        assert self.pdm.pronoun_set.count() == len(combs)
        
        # check the pronouns themselves...
        for comb in PronounType._generate_all_combinations():
            queryset = Pronoun.objects.filter(pronountype=comb)
            assert len(queryset) == 1, 'Got {0} not one'.format(len(queryset))
        
    def test_partial_prefill(self):
        # we should have a full complement.
        combs = PronounType._generate_all_combinations()
        assert self.pdm.pronoun_set.count() == len(combs)
        
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
        combs = PronounType._generate_all_combinations()
        missing = [_ for _ in combs if _.person == '2']
        assert len(missing) == 1
        assert self.pdm.pronoun_set.count() == (len(combs) - len(missing))
        
        # re-run prefill
        self.pdm._prefill_pronouns()
        
        # we should now have a full complement again.
        combs = PronounType._generate_all_combinations()
        assert self.pdm.pronoun_set.count() == len(combs)
        
        for pron in self.pdm.pronoun_set.all():
            if pron.pronountype.person == '2':
                assert pron.entries.count() == 0
            else:
                assert pron.entries.count() == 1
                assert pron.entries.all()[0].entry == 'old'
        
