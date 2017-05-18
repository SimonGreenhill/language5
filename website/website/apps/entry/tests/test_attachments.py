# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test.client import Client

from django.core.urlresolvers import reverse

from website.apps.core.models import Attachment
from website.apps.entry.models import Task

from website.apps.entry.tests import DataMixin

class Test_Attachment(DataMixin):
    """Tests the task image and task file get saved as attachments"""
    
    def setUp(self):
        self.client.login(username="admin", password="test")
        self.task.completable = True
        self.task.save()
    
    def test_attachment_is_linked_to_source(self):
        response = self.client.post(self.task.get_absolute_url(), self.form_data)
        t = Task.objects.get(pk=self.task.id)
        assert t.done
        assert Attachment.objects.count() == 1
        a = Attachment.objects.filter(source=t.source)[0]
        assert a.file.name == t.image.name # file names
    
