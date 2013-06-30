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
        
    def test_prefill(self):
        p = Paradigm.objects.create(language=self.lang, 
                                    source=self.source, 
                                    editor=self.editor,
                                    comment="test")
        p.save()
        
        # make sure the correct number of pronouns is there..
        assert len(p.pronoun_set.all()) == len(Pronoun._generate_all_combinations())
        
        # check the pronouns themselves...
        for comb in Pronoun._generate_all_combinations():
            queryset = Pronoun.objects.filter(
                paradigm = p,
                gender = None if comb['gender'] is None else comb['gender'][0],
                number = comb['number'][0],
                alignment = comb['alignment'][0],
                person = comb['person'][0]
            )
            assert len(queryset) == 1
        
        
    def test_partial_prefill(self):
        p = Paradigm.objects.create(language=self.lang, 
                                    source=self.source, 
                                    editor=self.editor,
                                    comment="test")
        p.save()
        # we should have a full complement. 
        assert len(p.pronoun_set.all()) == len(Pronoun._generate_all_combinations())
        
        # Let's delete some...
        for pron in p.pronoun_set.all():
            if pron.alignment == 'A':
                pron.delete()
            else:
                # modify the stored entries so we can identify them later.
                pron.form = Lexicon.objects.create(
                    editor=self.editor, 
                    source=self.source,
                    language=self.lang,
                    word=self.word,
                    entry="old"
                )
                pron.form.save()
                pron.save()
                
        # how many should we have deleted
        missing = [_ for _ in Pronoun._generate_all_combinations() if _['alignment'][0] == 'A']
        assert len(p.pronoun_set.all()) == (len(Pronoun._generate_all_combinations()) - len(missing))
        
        # re-run prefill
        p._prefill_pronouns()
        
        # we should now have a full complement again.
        assert len(p.pronoun_set.all()) == len(Pronoun._generate_all_combinations())
        
        for pron in p.pronoun_set.all():
            if pron.alignment == 'A':
                assert pron.form is None
            else:
                assert pron.form.entry == 'old'
        
