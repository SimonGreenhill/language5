# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test.client import Client

from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
from website.apps.entry.models import Task

from website.apps.entry.tests import DataMixin

class Test_Task_Saved(DataMixin):
    """Tests the Task Saved List"""
    def test_save(self):
        self.client.login(username="admin", password="test")
        response = self.client.post(self.task.get_absolute_url(), self.form_data, follow=True)
        self.assertRedirects(response,
            reverse('entry:complete', kwargs={'pk': self.task.id}), 
            status_code=302, target_status_code=200
        )
        self.assertTemplateUsed(response, 'entry/complete.html')
        
        the_task = Task.objects.get(pk=self.task.id)
        
        assert the_task.done
        
        assert the_task.lexicon.count() == 1
        assert the_task.lexicon.all()[0].entry == 'simon'
