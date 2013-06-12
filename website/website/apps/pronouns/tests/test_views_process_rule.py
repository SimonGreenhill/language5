from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import Q

from website.apps.core.models import Language, Source
from website.apps.pronouns.models import Paradigm, Pronoun, Rule, Relationship

from website.apps.pronouns.tests.test_views import DefaultSettingsMixin

class ProcessRuleMixin(DefaultSettingsMixin):
    def setUp(self):
        self.add_fixtures()
        self.url = reverse('pronouns:process_rule', kwargs={'paradigm_id': 1})
        self.client = Client()
        self.client.login(username='admin', password='test')
        self.response = self.client.get(self.url)
        
        self.expected_identicals = []
        for p in self.pdm.pronoun_set.all()[0:3]:
            p.form = 'I AM THE SAME'
            p.save()
            self.expected_identicals.append(p)
        
    def test_fail_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "%s?next=%s" % (reverse('login'), self.url))

    def test_fail_on_bad_pronoun_id(self):
        # have to do it this way (i.e. replace 1 with 100) or else `reverse`
        # raises a NoReverseMatch exception --> not what we're trying to test!
        response = self.client.get(self.url.replace("1", '100'))
        self.assertEqual(response.status_code, 404)
        
    def test_fail_on_nopost(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('pronouns:detail', kwargs={'paradigm_id': 1}))



    
class Test_ProcessRuleView_process_identicals(ProcessRuleMixin, TestCase):
    """Tests for first major action - processing identical items"""
    
    form_data = {
        'form-TOTAL_FORMS': u'10',
        'form-INITIAL_FORMS': u'10',
        'form-MAX_NUM_FORMS': u'1000',
        'process_identicals': 'true',
    }
    
    def test_saves_identicals(self):
        response = self.client.post(self.url, self.form_data)
        # successes will redirect to the edit_relationships view
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, 
            reverse('pronouns:edit_relationships', kwargs={'paradigm_id': 1}))
        rule = Rule.objects.all()[0]
        for p in self.expected_identicals:
            rel = Relationship.objects.filter(Q(pronoun1=p) | Q(pronoun2=p))
            assert len(rel) == 2, "Pronoun %d should have 2 relationships" % p.id
            for r in rel:
                assert r.pronoun1 in self.expected_identicals
                assert r.pronoun2 in self.expected_identicals
        
    def test_saves_rule(self):
        assert len(Rule.objects.all()) == 0, "Should start with no rules saved"
        response = self.client.post(self.url, self.form_data)
        # successes will redirect to the edit_relationships view
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, 
            reverse('pronouns:edit_relationships', kwargs={'paradigm_id': 1}))
        assert len(Rule.objects.all()) == 1, "Should have saved a rule"
        # get the saved rule & test it
        r = Rule.objects.all()[0]
        assert r.paradigm == self.pdm, "Rule should belong to this paradigm"
        assert 'Syncret' in r.rule, "Rule should mention syncretims"
    
    def test_save_relationship_set(self):
        response = self.client.post(self.url, self.form_data)
        # successes will redirect to the edit_relationships view
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, 
            reverse('pronouns:edit_relationships', kwargs={'paradigm_id': 1}))
        # get the saved rule & test relationsips
        r = Rule.objects.all()[0]
        assert len(r.relationships.all()) == 3, 'Was expecting 3 relationships'
        # test each relationship 
        for rel in r.relationships.all():
            assert rel.pronoun1 in self.expected_identicals
            assert rel.pronoun2 in self.expected_identicals
            
    def test_does_not_save_duplicates(self):
        response = self.client.post(self.url, self.form_data)
        response = self.client.post(self.url, self.form_data)
        rule = Rule.objects.all()[0]
        assert len(rule.relationships.all()) == 3, 'Was expecting 3 relationships'
        n = len(Relationship.objects.all()) 
        assert n == 3, "Expecting a total of 3 relationships, not %d" % n


class Test_ProcessRuleView_process_rules(ProcessRuleMixin, TestCase):
    """Tests for second major action - processing a ruleset"""
    
    def test_fails_on_bad_form(self):
        response = self.client.post(self.url, {'process_rule': 'true',})
        # redirect to the edit_relationships view
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, 
            reverse('pronouns:edit_relationships', kwargs={'paradigm_id': 1}))
        # no rule should be saved
        assert len(Rule.objects.all()) == 0
        
    def test_fails_on_invalid_rules_form(self):
        response = self.client.post(self.url, {
            'process_rule': 'true',
            ###'person_one': u'1', # No operand in set 1
            'person_two': u'12',
            'relationship': u'FO'
        })
        # redirect to the edit_relationships view
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, 
            reverse('pronouns:edit_relationships', kwargs={'paradigm_id': 1}))
        # no rule should be saved
        assert len(Rule.objects.all()) == 0

    def test_fails_on_invalid_rules_form_two(self):
        response = self.client.post(self.url, {
            'process_rule': 'true',
            'person_one': u'999', # invalid
            'person_two': u'12',
            'relationship': u'FO'
        })
        # redirect to the edit_relationships view
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, 
            reverse('pronouns:edit_relationships', kwargs={'paradigm_id': 1}))
        # no rule should be saved
        assert len(Rule.objects.all()) == 0
