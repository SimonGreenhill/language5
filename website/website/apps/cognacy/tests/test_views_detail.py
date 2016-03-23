from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from website.apps.cognacy.tests.data import DataMixin
from website.apps.lexicon.models import Word, WordSubset, Lexicon
from website.apps.lexicon.models import CognateSet, Cognate, CognateNote


class Test_CognateSetDetail(DataMixin, TestCase):
    def setUp(self):
        super(Test_CognateSetDetail, self).setUp()
        self.url = reverse('cognacy:detail', kwargs={'pk': self.cogset1.id})
    
    def test_200ok_logged_in(self):
        self.client.login(username="admin", password="test")
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
    
    def test_error_on_notlogged_in(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=%s" % self.url, 
                                    status_code=302, target_status_code=200)
    
    def test_get_missing(self):
        self.client.login(username="admin", password="test")
        response = self.client.get(reverse('cognacy:detail', kwargs={'pk': 5}))
        self.assertEquals(response.status_code, 404)
        
    def test_template(self):
        self.client.login(username="admin", password="test")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'cognacy/detail.html')
    
    def test_get_data(self):
        self.client.login(username="admin", password="test")
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        assert 'one' in response.content
        
        url = reverse('cognacy:detail', kwargs={'pk': self.cogset2.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        assert 'two' in response.content
        assert 'three' in response.content
        
    def test_notes(self):
        CognateNote.objects.create(cognateset=self.cogset1, note="I AM A NOTE", editor=self.editor)
        self.client.login(username="admin", password="test")
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        assert 'I AM A NOTE' in response.content
    
    def test_paginator(self):
        self.client.login(username="admin", password="test")
        response = self.client.get('{}?page=1'.format(self.url))
        self.assertEqual(response.status_code, 200)
    
    def test_bad_paginator_integer(self):
        self.client.login(username="admin", password="test")
        response = self.client.get('{}?page=10000'.format(self.url))
        self.assertEqual(response.status_code, 404)
        
    def test_bad_paginator_word(self):
        self.client.login(username="admin", password="test")
        response = self.client.get('{}?page=banana'.format(self.url))
        self.assertEqual(response.status_code, 404)
    
        