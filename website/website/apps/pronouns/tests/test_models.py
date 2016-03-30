from django.test import TestCase
from django.contrib.auth.models import User

from website.apps.core.models import Language, Source
from website.apps.lexicon.models import Word, Lexicon
from website.apps.pronouns.models import Paradigm, PronounType, Pronoun

from website.apps.pronouns.tests import PronounsTestData

class Test_PronounType(PronounsTestData, TestCase):
    def test_generate_all_combinations(self):
        combinations = PronounType._generate_all_combinations()
        assert combinations[0] == PronounType.objects.filter(person=1).get()
        assert combinations[1] == PronounType.objects.filter(person=2).get()
        assert combinations[2] == PronounType.objects.filter(person=3).get()


class Test_Paradigm(PronounsTestData, TestCase):
    def test_repr_no_label(self):
        assert unicode(self.pdm) == 'A'

    def test_repr_with_label(self):
        self.pdm.label = 'test'
        assert unicode(self.pdm) == 'A: test'
        
    def test_have_some_pronoun_types(self):
        assert self.pdm.pronoun_set.count() == 3
    
    def test_prefill(self):
        # make sure the correct number of pronouns is there..
        combs = PronounType._generate_all_combinations()
        assert self.pdm.pronoun_set.count() == len(combs)
        
        # check the pronouns themselves...
        for comb in PronounType._generate_all_combinations():
            count = Pronoun.objects.filter(pronountype=comb).count()
            assert count == 1, 'Got %d not one' % count
        
    def test_partial_prefill(self):
        # create new pdm
        pdm = Paradigm.objects.create(
            language=self.lang,
            source=self.source,
            editor=self.editor,
            comment="test_partial_prefill"
        )
        pdm._prefill_pronouns()
        
        # we should have a full complement.
        combs = PronounType._generate_all_combinations()
        assert pdm.pronoun_set.count() == len(combs)
        
        # Let's delete some...
        for pron in pdm.pronoun_set.all():
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
        assert pdm.pronoun_set.count() == (len(combs) - len(missing))
        
        # re-run prefill
        pdm._prefill_pronouns()
        
        # we should now have a full complement again.
        combs = PronounType._generate_all_combinations()
        assert pdm.pronoun_set.count() == len(combs)
        
        for pron in pdm.pronoun_set.all():
            if pron.pronountype.person == '2':
                assert pron.entries.count() == 0
            else:
                assert pron.entries.count() == 1
                assert pron.entries.all()[0].entry == 'old'
        
