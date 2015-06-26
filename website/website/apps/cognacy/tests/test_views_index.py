from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from website.apps.cognacy.tests.data import DataMixin

class Test_CognateSetIndex(DataMixin, TestCase):
    def setUp(self):
        super(Test_CognateSetIndex, self).setUp()
        self.url = reverse('cognacy:index')
    
    def test_200ok_logged_in(self):
        self.client.login(username="admin", password="test")
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
    
    def test_error_on_notlogged_in(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=%s" % self.url, 
                                    status_code=302, target_status_code=200)
    
    def test_template(self):
        self.client.login(username="admin", password="test")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'cognacy/index.html')
    
    def test_get_data(self):
        self.client.login(username="admin", password="test")
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        assert 'starts with t' in response.content
        assert 'starts with o' in response.content
        
