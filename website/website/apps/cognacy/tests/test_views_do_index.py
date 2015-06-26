from django.test import TestCase
from django.test.client import Client
from django.forms import ValidationError
from django.core.urlresolvers import reverse

from website.apps.cognacy.tests.data import DataMixin

class Test_Index(DataMixin):
    """Tests the Cognate List View"""
    url = reverse('cognacy:do_index')
    
    def test_template_used(self):
        self.client.login(username="admin", password="test")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'cognacy/do_index.html')
    
    def test_error_when_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302) 
        self.assertRedirects(response, 
                             "/accounts/login/?next=%s" % self.url, 
                             status_code=302, target_status_code=200)
        
    def test_ok_when_logged_in(self):
        self.client.login(username="admin", password="test")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_context_has_form(self):
        self.client.login(username="admin", password="test")
        response = self.client.get(self.url)
        assert 'form' in response.context
        
    def test_post(self):
        expected_url = reverse('cognacy:do', kwargs={'word': self.word.slug, 'clade': ''})
        self.client.login(username="admin", password="test")
        form_data = { 'word': self.word.id, 'submit': 'true',}
        response = self.client.post(self.url, form_data, follow=True)
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200)
         

