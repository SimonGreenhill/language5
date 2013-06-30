from django.test import TestCase

from website.apps.pronouns.models import Paradigm, Pronoun, Relationship

from website.apps.pronouns.tests import DefaultSettingsMixin

class Test_RelationshipManager_get_relationships_for_pronoun(DefaultSettingsMixin, TestCase):
    """Test the function get_relationships_for_pronoun on the RelationshipManager for Relationship"""
    def setUp(self):
        self.add_fixtures()
    
    def test_doesnt_find_anything_if_no_relationships(self):
        for p in self.pdm.pronoun_set.all():
            assert len(Relationship.objects.get_relationships_for_pronoun(p)) == 0
        
    def test_find_arg1(self):
        p1, p2 = self.pdm.pronoun_set.all()[0:2]
        rel = Relationship.objects.create(
            paradigm = self.pdm, pronoun1=p1, pronoun2=p2, relationship='TS',
            editor=self.editor
        )
        assert len(Relationship.objects.get_relationships_for_pronoun(p1)) == 1
        assert len(Relationship.objects.get_relationships_for_pronoun(p2)) == 1
        assert Relationship.objects.get_relationships_for_pronoun(p1)[0] == rel
        assert Relationship.objects.get_relationships_for_pronoun(p2)[0] == rel
        
    def test_find_arg2(self):
        p1, p2 = self.pdm.pronoun_set.all()[0:2]
        rel = Relationship.objects.create(
            paradigm = self.pdm, pronoun1=p2, pronoun2=p1, relationship='TS',
            editor=self.editor
        )
        assert len(Relationship.objects.get_relationships_for_pronoun(p2)) == 1
        assert len(Relationship.objects.get_relationships_for_pronoun(p1)) == 1
        assert Relationship.objects.get_relationships_for_pronoun(p2)[0] == rel
        assert Relationship.objects.get_relationships_for_pronoun(p1)[0] == rel
        

class Test_RelationshipManager_has_relationship_between(DefaultSettingsMixin, TestCase):
    """Test the function has_relationship_between on the RelationshipManager for Relationship"""
    def setUp(self):
        self.add_fixtures()
    
    def test_has_relationship_for_arg1(self):
        p1, p2 = self.pdm.pronoun_set.all()[0:2]
        rel = Relationship.objects.create(
            paradigm = self.pdm, pronoun1=p1, pronoun2=p2, relationship='TS',
            editor=self.editor
        )
        qset1 = Relationship.objects.has_relationship_between(p1, p2)
        qset2 = Relationship.objects.has_relationship_between(p2, p1)
        assert len(qset1) == 1
        assert len(qset2) == 1
        assert qset1[0] == rel
        assert qset1[0] == rel
        assert qset1[0].id == qset2[0].id
        
    def test_has_relationship_for_arg2(self):
        p1, p2 = self.pdm.pronoun_set.all()[0:2]
        rel = Relationship.objects.create(
            paradigm = self.pdm, pronoun1=p2, pronoun2=p1, relationship='TS',
            editor=self.editor
        )
        qset1 = Relationship.objects.has_relationship_between(p1, p2)
        qset2 = Relationship.objects.has_relationship_between(p2, p1)
        assert len(qset1) == 1
        assert len(qset2) == 1
        assert qset1[0] == rel
        assert qset1[0] == rel
        assert qset1[0].id == qset2[0].id
