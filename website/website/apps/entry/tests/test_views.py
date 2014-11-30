# -*- coding: utf-8 -*-
import re
from django.test import TestCase
from django.test.client import Client
from django.forms import ValidationError
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
from website.apps.core.models import Source, Language
from website.apps.lexicon.models import Word, Lexicon
from website.apps.entry.models import Task
from website.apps.entry.tests import DataMixin


class Test_TaskIndex(DataMixin):
    """Tests the TaskIndex view"""
    
    url = reverse('entry:index')
    
    def test_template_used(self):
        self.client.login(username="admin", password="test")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'entry/index.html')
    
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
    
    def test_context_has_quickform(self):
        self.client.login(username="admin", password="test")
        response = self.client.get(self.url)
        assert 'quickform' in response.context
        
    def test_shows_uncompleted_tasks(self):
        self.client.login(username="admin", password="test")
        response = self.client.get(self.url)
        self.assertContains(response, self.task.name, count=1)
        self.assertContains(response, self.task.get_absolute_url(), count=3)
        
    def test_hides_completed_tasks(self):
        self.client.login(username="admin", password="test")
        self.task.done = True
        self.task.save()
        response = self.client.get(self.url)
        assert self.task.name not in response
    

class Test_TaskComplete(DataMixin):
    """
    Tests the TaskComplete view
    
    (Also tested in tests_views_generic.py)
    """
    
    def test_template_used(self):
        self.client.login(username="admin", password="test")
        response = self.client.get(reverse('entry:complete', kwargs={'pk': self.task.id}))
        self.assertTemplateUsed(response, 'entry/complete.html')
    
    def test_error_when_not_logged_in(self):
        url = reverse('entry:complete', kwargs={'pk': self.task.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302) 
        self.assertRedirects(response, 
                             "/accounts/login/?next=%s" % url, 
                             status_code=302, target_status_code=200)
        
    def test_ok_when_logged_in(self):
        self.client.login(username="admin", password="test")
        url = reverse('entry:complete', kwargs={'pk': self.task.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_context_has_lexicon(self):
        self.client.login(username="admin", password="test")
        url = reverse('entry:complete', kwargs={'pk': self.task.id})
        response = self.client.get(url)
        assert 'lexicon' in response.context
