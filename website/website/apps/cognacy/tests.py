from django.test import TestCase

from django.test import TestCase
from django.test.client import Client
from django.forms import ValidationError
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
from website.apps.core.models import Language
from website.apps.lexicon.models import Word

class Test_Index(TestCase):
    """Tests the Cognate List View"""
    
    def setUp(self):
        self.url = reverse('cognacy:index')
        self.client = Client()
        self.editor = User.objects.create_user('admin',
                                               'admin@example.com', "test")
        self.lang = Language.objects.create(language='A', slug='langa', 
            information='i.1', classification='a, b',
            isocode='aaa', editor=self.editor)
        self.lang.save()
        self.word = Word.objects.create(word='Hand', slug='hand', 
            full='a hand', editor=self.editor)
        
        self.form_data = {
            'word': self.word.id,
            'submit': 'true',
        }
    
    def test_template_used(self):
        self.client.login(username="admin", password="test")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'cognacy/index.html')
    
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
        response = self.client.post(self.url, self.form_data, follow=True)
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200)
