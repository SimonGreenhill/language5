from django.test import TestCase

from website.apps.lexicon.models import Lexicon
from website.apps.pronouns.models import Paradigm, Pronoun, Relationship

from website.apps.pronouns.tests import DefaultSettingsMixin

class RelationshipMixin(DefaultSettingsMixin):
    def setUp(self):
        self.add_fixtures()
        self.p1, self.p2 = self.pdm.pronoun_set.all()[0:2]
        self.lex1 = Lexicon.objects.create(
                editor=self.editor, 
                source=self.source,
                language=self.lang,
                word=self.word,
                entry='I AM THE SAME'
            )
        self.lex2 = Lexicon.objects.create(
                editor=self.editor, 
                source=self.source,
                language=self.lang,
                word=self.word,
                entry='I AM THE SAME'
            )
        self.p1.entries.add(self.lex1)
        self.p1.save()
        
        self.p2.entries.add(self.lex2)
        self.p2.save()
        
        self.rel = Relationship.objects.create(
            paradigm = self.pdm, 
            pronoun1=self.p1, pronoun2=self.p2, 
            relationship='TS', editor=self.editor
        )
    

class Test_Relationship_get_pk_helper(RelationshipMixin, TestCase):
    """Tests the _get_pk helper function on Relationship"""
        
    def test_object(self):
        assert Relationship.objects._get_pk(self.p1) == self.p1.pk
        assert Relationship.objects._get_pk(self.p2) == self.p2.pk
        
    def test_integer(self):
        assert Relationship.objects._get_pk(int(self.p1.pk)) == self.p1.pk
        assert Relationship.objects._get_pk(int(self.p2.pk)) == self.p2.pk
        
    def test_something_else(self):
        with self.assertRaises(ValueError):
            Relationship.objects._get_pk('1')
            

class Test_RelationshipManager_get_relationships_for_pronoun(RelationshipMixin, TestCase):
    """Test the function get_relationships_for_pronoun on the RelationshipManager for Relationship"""
    def test_doesnt_find_anything_if_no_relationships(self):
        # note that the first 2 pronouns have relationships defined, skip them
        for p in self.pdm.pronoun_set.all()[2:]: 
            assert len(Relationship.objects.get_relationships_for_pronoun(p)) == 0
        
    def test_find_arg1_with_obj(self):
        assert len(Relationship.objects.get_relationships_for_pronoun(self.p1)) == 1
        assert len(Relationship.objects.get_relationships_for_pronoun(self.p2)) == 1
        assert Relationship.objects.get_relationships_for_pronoun(self.p1)[0] == self.rel
        assert Relationship.objects.get_relationships_for_pronoun(self.p2)[0] == self.rel
        
    def test_find_arg2_with_obj(self):
        assert len(Relationship.objects.get_relationships_for_pronoun(self.p2)) == 1
        assert len(Relationship.objects.get_relationships_for_pronoun(self.p1)) == 1
        assert Relationship.objects.get_relationships_for_pronoun(self.p2)[0] == self.rel
        assert Relationship.objects.get_relationships_for_pronoun(self.p1)[0] == self.rel
    
    def test_find_arg1_with_pk(self):
        assert len(Relationship.objects.get_relationships_for_pronoun(self.p1.id)) == 1
        assert len(Relationship.objects.get_relationships_for_pronoun(self.p2.id)) == 1
        assert Relationship.objects.get_relationships_for_pronoun(self.p1.id)[0] == self.rel
        assert Relationship.objects.get_relationships_for_pronoun(self.p2.id)[0] == self.rel
        
    def test_find_arg2_with_pk(self):
        assert len(Relationship.objects.get_relationships_for_pronoun(self.p2.id)) == 1
        assert len(Relationship.objects.get_relationships_for_pronoun(self.p1.id)) == 1
        assert Relationship.objects.get_relationships_for_pronoun(self.p2.id)[0] == self.rel
        assert Relationship.objects.get_relationships_for_pronoun(self.p1.id)[0] == self.rel
    

class Test_RelationshipManager_has_relationship_between(RelationshipMixin, TestCase):
    """Test the function has_relationship_between on the RelationshipManager for Relationship"""
    def test_has_relationship_for_arg1_with_obj(self):
        assert Relationship.objects.has_relationship_between(self.p1, self.p2)
        
    def test_has_relationship_for_arg2_with_obj(self):
        assert Relationship.objects.has_relationship_between(self.p2, self.p1)

    def test_has_relationship_for_arg1_with_pk(self):
        assert Relationship.objects.has_relationship_between(self.p1.pk, self.p2.pk)
        
    def test_has_relationship_for_arg2_with_pk(self):
        assert Relationship.objects.has_relationship_between(self.p2.pk, self.p1.pk)
