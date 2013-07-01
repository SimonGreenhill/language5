from django.test import TestCase

from website.apps.core.models import Language
from website.apps.lexicon.models import Lexicon
from website.apps.pronouns.models import Paradigm, Pronoun, Rule, Relationship
from website.apps.pronouns.tools import copy_paradigm
from website.apps.pronouns.tests import DefaultSettingsMixin


class TestCopyParadigm(DefaultSettingsMixin, TestCase):

    def setUp(self):
        self.add_fixtures()
        self.lang2 = Language.objects.create(language='B', 
                                             slug='langb', 
                                             information='', 
                                             classification='',
                                             isocode='bbb', 
                                             editor=self.editor)
        
    
    def test_no_paradigm_for_lang2(self):
        # haven't done anything, so no paradigm should exist for this language
        assert len(Paradigm.objects.filter(language=self.lang2)) == 0
        
    def test_adds_paradigm(self):
        newpdm = copy_paradigm(self.pdm, self.lang2)
        assert newpdm != self.pdm
        assert newpdm.language == self.lang2
    
    def test_adds_paradigm_doesnt_affect_previous(self):
        newpdm = copy_paradigm(self.pdm, self.lang2)
        assert self.pdm.language == self.lang
        assert self.pdm.pk is not None
        assert Paradigm.objects.get(pk=self.pdm.pk) == self.pdm
        
    def test_adds_rules(self):
        # create a rule on paradigm 1
        r1 = Rule.objects.create(paradigm=self.pdm, rule="Obey!", editor=self.editor)
        # make sure we saved that rule
        assert len(Rule.objects.filter(paradigm=self.pdm)) == 1, \
            "Should only have one rule"
        
        # now to test - 
        newpdm = copy_paradigm(self.pdm, self.lang2)
        
        assert newpdm != self.pdm, 'new paradigm should not be the same as the old one'
        
        # should now have a rule for paradigm 2
        r2 = Rule.objects.filter(paradigm=newpdm)
        assert len(r2) == 1, "Should have one rule for new paradigm"
        assert r2[0].rule == "Obey!", "Rule value has not been set"
        
        # do we still have our original rule?
        assert len(Rule.objects.filter(paradigm=self.pdm)) == 1
        assert Rule.objects.filter(paradigm=self.pdm)[0] == r1
        
        
    def test_adds_relationships(self):
        pronouns = self.pdm.pronoun_set.all()[0:3]
        
        # set the pronoun comment to something we can check later...
        for i, p in enumerate(pronouns):
            p.comment = str(i)
            p.save()
        
        # should have no relationships
        assert len(Relationship.objects.all()) == 0
        
        # create some relationships for paradigm 1
        rel1 = Relationship.objects.create(
            paradigm=self.pdm, pronoun1=pronouns[0], pronoun2=pronouns[1], 
            relationship='TS', editor=self.editor
        )
        rel2 = Relationship.objects.create(
            paradigm=self.pdm, pronoun1=pronouns[0], pronoun2=pronouns[2], 
            relationship='FO', editor=self.editor
        )
        
        # Relationships exist on paradigm 1 for 0 & 1 and 0 & 2
        # Should have 2 relationships
        assert len(Relationship.objects.all()) == 2
        
        p = copy_paradigm(self.pdm, self.lang2)
        
        assert p != self.pdm, 'new paradigm should not be the same as the old one'
        
        # Should have 4 relationships
        assert len(Relationship.objects.all()) == 4
        
        # test length
        newrels = p.relationship_set.all().order_by("pronoun1")
        assert len(newrels) == 2
        
        # have copied the relevant stuff?
        assert newrels[0].relationship == rel1.relationship == 'TS'
        assert newrels[1].relationship == rel2.relationship == 'FO'
        
        # check the new protoform comments to make sure they're right
        assert newrels[0].pronoun1.comment == '0', 'Expected 0 got %r' % newrels[0].pronoun1.comment
        assert newrels[0].pronoun2.comment == '1', 'Expected 1 got %r' % newrels[0].pronoun2.comment
        
        assert newrels[1].pronoun1.comment == '0', 'Expected 0 got %r' % newrels[0].pronoun1.comment
        assert newrels[1].pronoun2.comment == '2', 'Expected 2 got %r' % newrels[0].pronoun2.comment
        
    
    def test_adds_pronouns(self):
        
        count = Pronoun.objects.count()
        
        # update pronouns with the field `comment` set to the PK.
        old_pronouns = {}
        for p in self.pdm.pronoun_set.all():
            p.comment = str(p.pk)
            p.save()
            old_pronouns[p.pk] = p
        
        newpdm = copy_paradigm(self.pdm, self.lang2)
        
        assert newpdm != self.pdm, 'new paradigm should not be the same as the old one'
        
        assert Pronoun.objects.count() == (count * 2), \
            "Should have twice as many pronouns now, %r not %r" % (count*2, Pronoun.objects.count())
        
        # loop over new pronouns and check that they match their ancestral object
        # in all attributes. Remember the ancestral PK is stored in `comment`
        for new_p in newpdm.pronoun_set.all():
            pk = int(new_p.comment)
            assert pk in old_pronouns
            old_p = old_pronouns[pk]
            
            for attr in ('person', 'number', 'gender', 'alignment'):
                assert getattr(new_p, attr) == getattr(old_p, attr)
            
            # check paradigm
            assert new_p.paradigm == newpdm
            assert old_p.paradigm == self.pdm
    
    def test_adds_pronoun_form_sets(self):
        
        def _make_token(p):
            return "%s-%s-%s-%s" % (p.person, p.number, p.gender, p.alignment)
            
        def _break_token(p):
            keys = ['person', 'number', 'gender', 'alignment']
            values = []
            for v in p.split("-"):
                if v == u'None':
                    v = None
                values.append(v)
            return dict(zip(keys, values))
        
        # go through old paradigm, add some lexical items to each.
        for pron in self.pdm.pronoun_set.all():
            pron.entries.add(
                Lexicon.objects.create(
                    editor=self.editor, 
                    source=self.source,
                    language=self.lang,
                    word=self.word,
                    entry=_make_token(pron)
                )
            )
        
        # copy paradigm...
        newpdm = copy_paradigm(self.pdm, self.lang2)
        
        # check old paradigm
        for pron in self.pdm.pronoun_set.all():
            assert pron.entries.count() == 1, "Should have one pronoun form"
            lex_obj = pron.entries.all()[0]
            # check language is correct!
            assert lex_obj.language == self.pdm.language, \
                "Language should still be %s" % self.pdm.language
            
            # check other attributes
            values = _break_token(lex_obj.entry)
            for attr in values:
                assert values[attr] == getattr(pron, attr)
            
        # check new paradigm
        for pron in newpdm.pronoun_set.all():
            assert pron.entries.count() == 1, "Should have one pronoun form"
            lex_obj = pron.entries.all()[0]
            
            # check language is correct!
            assert lex_obj.language == self.lang2, \
                "Language should be changed to %s" % self.lang2
            
            # check other attributes
            values = _break_token(lex_obj.entry)
            for attr in values:
                assert values[attr] == getattr(pron, attr)
            