from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.db.models import Q

from website.apps.lexicon.models import Lexicon
from website.apps.pronouns.models import Rule, Relationship, Paradigm
from website.apps.pronouns.tests import PronounsTestData


class ProcessRuleMixin(PronounsTestData):
    @classmethod
    def setUpTestData(cls):
        super(ProcessRuleMixin, cls).setUpTestData()
        cls.rulepdm = Paradigm.objects.create(
            language=cls.lang,
            source=cls.source,
            editor=cls.editor,
            comment="ProcessRuleMixin"
        )
        cls.rulepdm._prefill_pronouns()
        
        cls.expected_identicals = []
        for pron in cls.rulepdm.pronoun_set.all():
            lex = Lexicon.objects.create(
                editor=cls.editor,
                language=cls.lang,
                source=cls.source,
                word=cls.word,
                entry='ProcessRuleMixin'
            )
            lex.save()
            pron.entries.add(lex)
            pron.save()
            cls.expected_identicals.append(pron)
        
        cls.client = Client()
        cls.url = reverse('pronouns:process_rule', kwargs={'paradigm_id': cls.rulepdm.id})
        
    
    def test_fail_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, "%s?next=%s" % (reverse('login'), self.url)
        )

    def test_fail_on_nopost(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse('pronouns:detail', kwargs={'paradigm_id': self.rulepdm.id})
        )


class Test_ProcessRuleView_process_identicals(ProcessRuleMixin, TestCase):
    """Tests for first major action - processing identical items"""
    
    form_data = {
        'form-TOTAL_FORMS': u'10',
        'form-INITIAL_FORMS': u'10',
        'form-MAX_NUM_FORMS': u'1000',
        'process_identicals': 'true',
    }
    
    def setUp(self):
        self.client.login(username='admin', password='test')
        self.response = self.client.get(self.url)
    
    def test_saves_identicals(self):
        response = self.client.post(self.url, self.form_data)
        # successes will redirect to the edit_relationships view
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse('pronouns:edit_relationships', kwargs={'paradigm_id': self.rulepdm.id})
        )
        
        assert Rule.objects.count() == 1, "should have saved a rule"
        
        for p in self.expected_identicals:
            rel = Relationship.objects.filter(Q(pronoun1=p) | Q(pronoun2=p))
            
            if len(rel) != 2:
                raise AssertionError(
                    "Pronoun %d should have 2 relationships" % p.id
                )
            for r in rel:
                assert r.pronoun1 in self.expected_identicals
                assert r.pronoun2 in self.expected_identicals
        
    def test_saves_rule(self):
        response = self.client.post(self.url, self.form_data)
        # successes will redirect to the edit_relationships view
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse('pronouns:edit_relationships', kwargs={'paradigm_id': self.rulepdm.id})
        )
        
        assert Rule.objects.count() == 1, "should have saved a rule"
        
        # get the saved rule & test it
        r = Rule.objects.all()[0]
        assert r.paradigm == self.rulepdm, "Rule should belong to this paradigm"
        assert 'Syncret' in r.rule, "Rule should mention syncretims"
    
    def test_save_relationship_set(self):
        response = self.client.post(self.url, self.form_data)
        # successes will redirect to the edit_relationships view
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse('pronouns:edit_relationships', kwargs={'paradigm_id': self.rulepdm.id})
        )
        
        assert Rule.objects.count() == 1, "should have saved a rule"
        # get the saved rule & test relationsips
        r = Rule.objects.all()[0]
        assert len(r.relationships.all()) == 3, 'Was expecting 3 relationships'
        # test each relationship
        for rel in r.relationships.all():
            assert rel.pronoun1 in self.expected_identicals
            assert rel.pronoun2 in self.expected_identicals
            
    def test_does_not_save_duplicates(self):
        for i in range(0, 2):
            response = self.client.post(self.url, self.form_data)
            self.assertEqual(response.status_code, 302)
            redir_url = reverse(
                'pronouns:edit_relationships', kwargs={'paradigm_id': self.rulepdm.id}
            )
            self.assertRedirects(response, redir_url)
        
        rule = Rule.objects.get(pk=self.rulepdm.pk)
        import IPython; IPython.embed()
        assert len(rule.relationships.all()) == 3


class Test_ProcessRuleView_process_rules(ProcessRuleMixin, TestCase):
    """Tests for second major action - processing a ruleset"""
    
    def setUp(self):
        self.editrel_url = reverse(
            'pronouns:edit_relationships', kwargs={'paradigm_id': self.rulepdm.id}
        )
        self.client.login(username='admin', password='test')
        self.response = self.client.get(self.url)

    
    def test_fails_on_bad_form(self):
        response = self.client.post(self.url, {'process_rule': 'true', })
        # redirect to the edit_relationships view
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.editrel_url)
        # no rule should be saved
        assert Rule.objects.count() == 0
        
    def test_fails_on_invalid_rules_form(self):
        response = self.client.post(self.url, {
            'process_rule': 'true',
            ###'person_one': u'1', # No operand in set 1
            'person_two': u'12',
            'relationship': u'FO'
        })
        # redirect to the edit_relationships view
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.editrel_url)
        # no rule should be saved
        assert Rule.objects.count() == 0

    def test_fails_on_invalid_rules_form_two(self):
        response = self.client.post(self.url, {
            'process_rule': 'true',
            'person_one': u'999',  # invalid
            'person_two': u'12',
            'relationship': u'FO'
        })
        # redirect to the edit_relationships view
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.editrel_url)
        # no rule should be saved
        assert Rule.objects.count() == 0
