from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from website.apps.core.models import Language, Source
from website.apps.lexicon.models import Lexicon
from website.apps.pronouns.models import Paradigm, Pronoun
from website.apps.pronouns.tools import full_repr_row

from website.apps.pronouns.tests import DefaultSettingsMixin


class Test_Paradigm(DefaultSettingsMixin, TestCase):
    def setUp(self):
        self.add_fixtures()
        self.p = Paradigm.objects.create(language=self.lang, 
                                    source=self.source, 
                                    editor=self.editor,
                                    comment="test")
        self.p.save()
        
    def test_prefill(self):
        
        # make sure the correct number of pronouns is there..
        assert len(self.p.pronoun_set.all()) == len(Pronoun._generate_all_combinations())
        
        # check the pronouns themselves...
        for comb in Pronoun._generate_all_combinations():
            queryset = Pronoun.objects.filter(
                paradigm = self.p,
                gender = None if comb['gender'] is None else comb['gender'][0],
                number = comb['number'][0],
                alignment = comb['alignment'][0],
                person = comb['person'][0]
            )
            assert len(queryset) == 1
        
        
    def test_partial_prefill(self):
        # we should have a full complement. 
        assert len(self.p.pronoun_set.all()) == len(Pronoun._generate_all_combinations())
        
        # Let's delete some...
        for pron in self.p.pronoun_set.all():
            if pron.alignment == 'A':
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
        missing = [_ for _ in Pronoun._generate_all_combinations() if _['alignment'][0] == 'A']
        assert len(self.p.pronoun_set.all()) == (len(Pronoun._generate_all_combinations()) - len(missing))
        
        # re-run prefill
        self.p._prefill_pronouns()
        
        # we should now have a full complement again.
        assert len(self.p.pronoun_set.all()) == len(Pronoun._generate_all_combinations())
        
        for pron in self.p.pronoun_set.all():
            if pron.alignment == 'A':
                assert pron.entries.count() == 0
            else:
                assert pron.entries.count() == 1
                assert pron.entries.all()[0].entry == 'old'
        
