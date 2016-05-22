from django.test import TestCase

from website.apps.lexicon.models import Lexicon
from website.apps.pronouns.models import Paradigm, PronounType, Pronoun, Relationship

from website.apps.pronouns.tests import PronounsTestData

class Test_PronounType(PronounsTestData, TestCase):
    def test_generate_all_combinations(self):
        combinations = PronounType._generate_all_combinations()
        assert combinations[0] == PronounType.objects.filter(person=1).get()
        assert combinations[1] == PronounType.objects.filter(person=2).get()
        assert combinations[2] == PronounType.objects.filter(person=3).get()


class Test_Paradigm(PronounsTestData, TestCase):
    def test_repr_no_label(self):
        pdm = Paradigm(
            language=self.lang,
            source=self.source,
            editor=self.editor,
            label="",
        )
        assert unicode(pdm) == 'A', "Got: %s" % unicode(pdm)

    def test_repr_with_label(self):
        pdm = Paradigm(
            language=self.lang,
            source=self.source,
            editor=self.editor,
            label="label",
        )
        assert unicode(pdm) == 'A: label', "Got: %s" % unicode(pdm)
        
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


class TestRelationship(PronounsTestData, TestCase):
    #Tests the _get_pk helper function on Relationship
    def test_get_pk_object(self):
        assert Relationship.objects._get_pk(self.p1) == self.p1.pk
        assert Relationship.objects._get_pk(self.p2) == self.p2.pk

    def test_get_pk_integer(self):
        assert Relationship.objects._get_pk(int(self.p1.pk)) == self.p1.pk
        assert Relationship.objects._get_pk(int(self.p2.pk)) == self.p2.pk

    def test_get_pk_something_else(self):
        with self.assertRaises(ValueError):
            Relationship.objects._get_pk('1')

    #Test get_relationships_for_pronoun on the RelationshipManager for Relationship
    def _grfp(self, p):
        # helper
        return Relationship.objects.get_relationships_for_pronoun(p)

    def test_grfp_doesnt_find_anything_if_no_relationships(self):
        # note that the first 2 pronouns have relationships defined, skip them
        for p in self.pdm.pronoun_set.all()[2:]:
            assert len(self._grfp(p)) == 0

    def test_grfp_find_arg1_with_obj(self):
        assert len(self._grfp(self.p1)) == 1
        assert len(self._grfp(self.p2)) == 1
        assert self._grfp(self.p1)[0] == self.rel
        assert self._grfp(self.p2)[0] == self.rel

    def test_grfp_find_arg2_with_obj(self):
        assert len(self._grfp(self.p2)) == 1
        assert len(self._grfp(self.p1)) == 1
        assert self._grfp(self.p2)[0] == self.rel
        assert self._grfp(self.p1)[0] == self.rel

    def test_grfp_find_arg1_with_pk(self):
        assert len(self._grfp(self.p1.id)) == 1
        assert len(self._grfp(self.p2.id)) == 1
        assert self._grfp(self.p1.id)[0] == self.rel
        assert self._grfp(self.p2.id)[0] == self.rel

    def test_grfp_find_arg2_with_pk(self):
        assert len(self._grfp(self.p2.id)) == 1
        assert len(self._grfp(self.p1.id)) == 1
        assert self._grfp(self.p2.id)[0] == self.rel
        assert self._grfp(self.p1.id)[0] == self.rel

    # Test the function has_relationship_between on the RelationshipManager for
    # Relationship
    def test_has_relationship_for_arg1_with_obj(self):
        assert Relationship.objects.has_relationship_between(
            self.p1, self.p2
        )

    def test_has_relationship_for_arg2_with_obj(self):
        assert Relationship.objects.has_relationship_between(
            self.p2, self.p1
        )

    def test_has_relationship_for_arg1_with_pk(self):
        assert Relationship.objects.has_relationship_between(
            self.p1.pk, self.p2.pk
        )

    def test_has_relationship_for_arg2_with_pk(self):
        assert Relationship.objects.has_relationship_between(
            self.p2.pk, self.p1.pk
        )
