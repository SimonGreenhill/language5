# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from website.apps.entry.models import Task, TaskLog

from website.apps.entry.tests import DataMixin

class Test_GenericView(DataMixin):
    """Tests the GenericView Detail Page"""
    
    def test_index_logging(self):
        assert TaskLog.objects.count() == 0
        self.client.login(username="admin", password="test")
        self.client.get(reverse('entry:index'))
        assert TaskLog.objects.count() == 1
    
    def test_page_logging(self):
        assert TaskLog.objects.count() == 0
        self.client.login(username="admin", password="test")
        self.client.get(self.task.get_absolute_url())
        assert TaskLog.objects.count() == 1
    
    def test_save_logging(self):
        self.client.login(username="admin", password="test")
        
        assert TaskLog.objects.count() == 0
        
        response = self.client.post(self.task.get_absolute_url(), self.form_data)
        
        assert TaskLog.objects.count() > 0
        