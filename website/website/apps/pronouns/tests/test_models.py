from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from website.apps.core.models import Language, Source
from website.apps.lexicon.models import Word, Lexicon
from website.apps.pronouns.models import Paradigm, PronounType, Pronoun

class Test_PronounType(TestCase):
    def setUp(self):
        self.editor = User.objects.create_user('admin', 'admin@admin.com', "test")
        self.lang = Language.objects.create(language='A', slug='langa', 
                                             information='i.1', 
                                             classification='a, b',
                                             isocode='aaa', editor=self.editor)
        self.source = Source.objects.create(year="1991", author='Smith', 
                                 slug='Smith1991', reference='S2',
                                 comment='c1', editor=self.editor)
        self.word = Word.objects.create(word='Pronoun', slug='apronoun', 
                                        full='pronoun', editor=self.editor)
                                        
        # add some pronoun types
        for person in [1, 2, 3]:
            w = Word.objects.create(
                word="pronoun-a-%d-sg" % person,
                slug="pronoun-a-%d-sg" % person,
                editor=self.editor
            )
            w.save()
            p = PronounType.objects.create(
                word=w, 
                alignment='A', person=person, number='sg',
                sequence = person, # dummy
                editor=self.editor
            )
            if person == 2: # PERSON 2 should be hidden!
                p.active = False
            else:
                p.active = True
            p.save()
    
    def test_count(self):
        assert PronounType.objects.count() == 2
    
    def test_generate_all_combinations(self):
        combinations = PronounType._generate_all_combinations()
        assert combinations[0] == PronounType.objects.filter(person=1).get()
        assert combinations[1] == PronounType.objects.filter(person=3).get()
    
    def test_paradigm_create(self):
        pdm = Paradigm.objects.create(language=self.lang, 
                                 source=self.source, 
                                 editor=self.editor,
                                 comment="test")
        pdm._prefill_pronouns()
        
        # make sure the correct number of pronouns is there..
        assert pdm.pronoun_set.count() == 2
        
        # check the pronouns themselves...
        for comb in PronounType._generate_all_combinations():
            queryset = Pronoun.objects.filter(pronountype=comb)
            assert len(queryset) == 1, 'Got {0} not one'.format(len(queryset))
        
