from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

class Test_Robots_Txt(TestCase):
    """Tests the robots.txt page"""
    client = Client()
    url = reverse("robots_txt")
    
    def setUp(self):
        self.response = self.client.get(self.url)
    
    def test_request(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'robots.txt')
    
    def test_content(self):
        self.assertContains(self.response, 'User-agent')
        
        
