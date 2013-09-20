from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from website.apps.lexicon.models import Lexicon
from website.apps.pronouns.tools import full_repr_row
from website.apps.pronouns.models import Paradigm, PronounType, Pronoun
from website.apps.pronouns.tests import DefaultSettingsMixin


# Test View: Edit paradigm
class Test_EditParadigmView(DefaultSettingsMixin, TestCase):
    
    def setUp(self):
        self.add_fixtures()
        self.url = reverse('pronouns:edit', kwargs={'paradigm_id': self.pdm.id})
        self.client = Client()
        self.client.login(username='admin', password='test')
        self.response = self.client.get(self.url)
    
    def test_200ok(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'pronouns/edit.html')
    
    def test_fail_when_not_logged_in(self):
        self.assertEqual(self.client.get(self.url).status_code, 200)
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "%s?next=%s" % (reverse('login'), 
            reverse("pronouns:edit", kwargs={'paradigm_id': self.pdm.id})))
        
    def test_form_generation(self):
        form = self.response.context['pronouns']
        raise NotImplementedError("Not Implemented")
    
    def test_form_load(self):
        raise NotImplementedError("Not Implemented")
        
    def test_form_save(self):
        raise NotImplementedError("Not Implemented")