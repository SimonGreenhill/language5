# -*- coding: utf-8 -*-
import json
from django.test import TestCase
from django.test.client import Client

from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
from website.apps.core.models import Source, Language
from website.apps.lexicon.models import Word, Lexicon
from website.apps.entry.models import Task
from website.apps.entry.dataentry import available_views

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
            image=self.file_testimage,
            done=False,
            view="GenericView",
            records=1, # needed so we don't have too many empty forms to validate
        )
        
        self.lang = Language.objects.create(language='A', slug='langa', 
            information='i.1', classification='a, b',
            isocode='aaa', editor=self.editor)
            
        self.word = Word.objects.create(word='Hand', slug='hand', 
            full='a hand', editor=self.editor)
            
        # for formset validation
        self.form_data = {
            'form-TOTAL_FORMS': u'1',
            'form-INITIAL_FORMS': u'0',
            'form-MAX_NUM_FORMS': u'1000',
            'form-1-language': self.lang.id,
            'form-1-source': self.source.id,
            'form-1-word': self.word.id,
            'form-1-entry': 'simon',
            'form-1-annotation': 'comment',
        }
        
        
    def test_testimage_is_present(self):
        """
        This test makes sure that the test image is present on the file-system
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
        self.assertRedirects(response, reverse('entry:index'), status_code=302, target_status_code=200)
    
    def test_number_of_records(self):
        self.client.login(username="admin", password="test")
        response = self.client.get(self.task.get_absolute_url())
        assert len(response.context['formset'].forms) == 1
        
        self.task.records = 2
        self.task.save()
        
        response = self.client.get(self.task.get_absolute_url())
        assert len(response.context['formset'].forms) == 2
        
    def test_post_does_not_set_done_if_not_completable(self):
        self.client.login(username="admin", password="test")
        self.task.completable = False
        self.task.save()
        response = self.client.get(self.task.get_absolute_url())
        response = self.client.post(self.task.get_absolute_url(), self.form_data)
        
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entry/done.html')
        assert not Task.objects.get(pk=self.task.id).done

    def test_post_sets_done_if_completable(self):
        self.client.login(username="admin", password="test")
        self.task.completable = True
        self.task.save()
        response = self.client.post(self.task.get_absolute_url(), self.form_data)
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entry/done.html')
        assert Task.objects.get(pk=self.task.id).done
    
        