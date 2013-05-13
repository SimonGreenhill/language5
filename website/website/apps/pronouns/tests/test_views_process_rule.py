from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from website.apps.core.models import Language, Source
from website.apps.pronouns.models import Paradigm, Pronoun

from website.apps.pronouns.tests.test_views import DefaultSettingsMixin

class ExtraSettingsMixin(DefaultSettingsMixin):
    def setUp(self):
        self.add_fixtures()
        self.pdm = Paradigm.objects.create(language=self.lang, 
                                    source=self.source, 
                                    editor=self.editor,
                                    comment="test")
        
        self.url = reverse('pronouns:process_rule', kwargs={'paradigm_id': 1})
        self.client = Client()
        self.client.login(username='admin', password='test')
        self.response = self.client.get(self.url)
    
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



    
class Test_ProcessRuleView_process_identicals(ExtraSettingsMixin, TestCase):
    """Tests for first major action - processing identical items"""
        
    def test_saves_identicals(self):
        assert False
        
    def test_saves_rule(self):
        assert False
    
    def test_save_relationship_set(self):
        assert False


class Test_ProcessRuleView_process_rules(ExtraSettingsMixin, TestCase):
    """Tests for second major action - processing a ruleset"""
    def test_fail_on_nopost(self):
        assert False

    
