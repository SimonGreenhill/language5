# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test.client import Client

from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
from website.apps.core.models import Source
from website.apps.entry.models import Task

from website.apps.entry.forms import entry_forms


class Test_Detail(TestCase):
    """Tests the Detail Page"""
    
    def setUp(self):
        self.client = Client()
        # some data
        self.file_testimage = "data/2013-01/test.png"
        self.editor = User.objects.create_user('admin',
                                               'admin@example.com', "test")
        self.source = Source.objects.create(
                year=1991,
                author='Smith',
                slug='Smith1991',
                reference='S2',
                comment='c1',
                editor=self.editor
        )
        self.task = Task.objects.create(
            editor=self.editor,
            name="Test Task",
            description="A Test of Data Entry",
            source=self.source,
            form=entry_forms[0],
            image=self.file_testimage,
            done=False
        )
    
    def test_testimage_is_present(self):
        """
        This test makes sure that the test image 
        is present on the file-system
        """
        from os.path import join, isfile
        from django.conf import settings
        test_file = join(settings.MEDIA_ROOT, self.file_testimage)
        assert isfile(test_file), \
                """Missing Test Image File on File-System at %s! 
                   Other tests will fail!""" % test_file
        
    def test_error_when_not_logged_in(self):
        response = self.client.get(self.task.get_absolute_url())
        self.failUnlessEqual(response.status_code, 302) 
        self.assertRedirects(response, 
                             "/accounts/login/?next=%s" % self.task.get_absolute_url(), 
                             status_code=302, target_status_code=200)
        
    def test_ok_when_logged_in(self):
        self.client.login(username="admin", password="test")
        response = self.client.get(self.task.get_absolute_url())
        self.failUnlessEqual(response.status_code, 200)
        
    def test_active_task(self):
        self.client.login(username="admin", password="test")
        response = self.client.get(self.task.get_absolute_url())
        self.failUnlessEqual(response.status_code, 200)
        
    def test_completed_task(self):
        self.client.login(username="admin", password="test")
        self.task.done = True
        self.task.save()
        response = self.client.get(self.task.get_absolute_url())
        self.assertRedirects(response, reverse('task-index'), status_code=302, target_status_code=200)
        
    
