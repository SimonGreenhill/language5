from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

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

    def test_disallows_sort_permutations(self):
        # closes the crawler trap for well-behaved bots
        self.assertContains(self.response, 'Disallow: /*?*sort=')

    def test_disallows_page_permutations(self):
        self.assertContains(self.response, 'Disallow: /*?*page=')

    def test_has_crawl_delay(self):
        self.assertContains(self.response, 'Crawl-delay:')
        
        

    def test_disallows_private_sections(self):
        for path in ('/admin/', '/entry/', '/cognacy/', '/accounts/'):
            self.assertContains(self.response, 'Disallow: %s\n' % path)
