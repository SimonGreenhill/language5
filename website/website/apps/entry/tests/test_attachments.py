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
        super(Test_Attachment, self).setUp()
        self.task.language = self.lang
    
    def test_attachment_is_linked_to_source(self):
        self.client.login(username="admin", password="test")
        self.task.completable = True
        self.task.save()
        response = self.client.post(self.task.get_absolute_url(), self.form_data)
        t = Task.objects.get(pk=self.task.id)
        assert t.done
        assert Attachment.objects.count() == 1
        a = Attachment.objects.filter(source=t.source)[0]
        assert a.file.name == t.image.name # file names
    
    def test_task_image_is_attached(self):
        self.client.login(username="admin", password="test")
        self.task.completable = True
        self.task.save()
        response = self.client.post(self.task.get_absolute_url(), self.form_data)
        t = Task.objects.get(pk=self.task.id)
        assert t.done
        assert Attachment.objects.count() == 1
        a = Attachment.objects.filter(language=t.language)[0]
        
        assert a.file.name == t.image.name # file names
        assert a.file.file.name == t.image.file.name # file paths
        assert a.file.read() == t.image.file.read() # file content
        
    def test_task_file_is_attached(self):
        self.client.login(username="admin", password="test")
        self.task.completable = True
        # move the image to be stored in file.
        self.task.file = self.task.image
        self.task.image = None
        self.task.save()
        
        response = self.client.post(self.task.get_absolute_url(), self.form_data)
        t = Task.objects.get(pk=self.task.id)
        assert t.done
        assert Attachment.objects.count() == 1
        a = Attachment.objects.filter(language=t.language)[0]
        
        assert a.file.name == t.file.name # file names
        assert a.file.file.name == t.file.file.name # file paths
        assert a.file.read() == t.file.file.read() # file content
        