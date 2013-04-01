# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test.client import Client

from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
from website.apps.core.models import Source, Language
from website.apps.lexicon.models import Word
from website.apps.entry.models import Task
from website.apps.entry.dataentry import available_views

class Test_Detail(TestCase):
    """Tests the Detail Page"""
    
    def setUp(self):
        self.client = Client()
        # for formset validation
        self.management_data = {
            'form-TOTAL_FORMS': u'20',
            'form-INITIAL_FORMS': u'0',
            'form-MAX_NUM_FORMS': u'1000',
        }
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
            done=False
        )
        
        self.lang = Language.objects.create(language='A', slug='langa', 
            information='i.1', classification='a, b',
            isocode='aaa', editor=self.editor)
        
        self.word = Word.objects.create(word='Hand', slug='hand', 
            full='a hand', editor=self.editor)
        
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
        self.assertRedirects(response, reverse('entry:index'), status_code=302, target_status_code=200)
        
    def test_post_sets_done(self):
        self.client.login(username="admin", password="test")
        response = self.client.get(self.task.get_absolute_url())
        
        vars = self.management_data.copy()
        vars['form-1-language'] = self.lang.id
        vars['form-1-source'] = self.source.id
        vars['form-1-word'] = self.word.id
        vars['form-1-entry'] = 'simon'
        vars['form-1-annotation'] = 'is awesome'
        
        response = self.client.post(self.task.get_absolute_url(), vars)
        self.failUnlessEqual(response.status_code, 200)
        assert Task.objects.get(pk=self.task.id).done
    
    def test_post_saves(self):
        self.client.login(username="admin", password="test")
        response = self.client.get(self.task.get_absolute_url())
        
        vars = self.management_data.copy()
        vars['form-1-language'] = self.lang.id
        vars['form-1-source'] = self.source.id
        vars['form-1-word'] = self.word.id
        vars['form-1-entry'] = 'simon'
        vars['form-1-annotation'] = 'is awesome'
        
        response = self.client.post(self.task.get_absolute_url(), vars)
        
        self.failUnlessEqual(response.status_code, 200)
        from website.apps.lexicon.models import Lexicon
        
        l = Lexicon.objects.get(pk=1)
        assert l.language == self.lang
        assert l.source == self.source
        assert l.word == self.word
        assert l.entry == 'simon'
        assert l.annotation == 'is awesome'

