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


class Test_GenericView(DataMixin):
    """Tests the GenericView Detail Page"""
    
    def test_template_used(self):
        self.client.login(username="admin", password="test")
        response = self.client.get(self.task.get_absolute_url())
        self.assertTemplateUsed(response, 'entry/detail.html')
    
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
        self.assertEqual(response.status_code, 302) 
        self.assertRedirects(response, 
                             "/accounts/login/?next=%s" % self.task.get_absolute_url(), 
                             status_code=302, target_status_code=200)
        
    def test_ok_when_logged_in(self):
        self.client.login(username="admin", password="test")
        response = self.client.get(self.task.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        
    def test_active_task(self):
        self.client.login(username="admin", password="test")
        response = self.client.get(self.task.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        
    def test_completed_task(self):
        self.client.login(username="admin", password="test")
        self.task.done = True
        self.task.save()
        response = self.client.get(self.task.get_absolute_url())
        self.assertRedirects(response, 
            reverse('entry:complete', kwargs={'pk': self.task.id}), 
            status_code=302, target_status_code=200
        )
        
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
        response = self.client.post(self.task.get_absolute_url(), self.form_data)
        assert not Task.objects.get(pk=self.task.id).done
    
    def test_post_sets_done_if_completable(self):
        self.client.login(username="admin", password="test")
        self.task.completable = True
        self.task.save()
        response = self.client.post(self.task.get_absolute_url(), self.form_data)
        assert Task.objects.get(pk=self.task.id).done
    
    def test_unfixed_language_in_template(self):
        self.client.login(username="admin", password="test")
        task = Task.objects.create(
            editor=self.editor,
            name="Test Task - Fixed Language",
            description="",
            source=self.source,
            done=False,
            view="GenericView",
            records=1, # needed so we don't have too many empty forms to validate
        )
        response = self.client.get(task.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entry/detail.html')
        self.assertTemplateUsed(response, 'entry/formtemplates/generic.html')
        self.assertContains(response, '<option value="1">A</option>', count=1)
        self.assertContains(response, 'form-0-language', count=3)
        
    def test_fixed_language_in_template(self):
        self.client.login(username="admin", password="test")
        self.lang.language = "TEST LANGUAGE"
        self.lang.save()
        
        task = Task.objects.create(
            editor=self.editor,
            name="Test Task - Fixed Language",
            description="",
            language=self.lang,
            source=self.source,
            done=False,
            view="GenericView",
            records=1, # needed so we don't have too many empty forms to validate
        )
        response = self.client.get(task.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entry/detail.html')
        self.assertTemplateUsed(response, 'entry/formtemplates/generic.html')
        self.assertContains(response, 
            '<input id="id_form-0-language" name="form-0-language" type="hidden" value="1" />', 
            count=1
        )
    
    def test_fixed_source_in_template(self):
        self.client.login(username="admin", password="test")
        self.source.author = "TEST SOURCE"
        self.source.save()
        task = Task.objects.create(
            editor=self.editor,
            name="Test Task - Fixed Language",
            description="",
            language=self.lang,
            source=self.source,
            done=False,
            view="GenericView",
            records=1, # needed so we don't have too many empty forms to validate
        )
        response = self.client.get(task.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entry/detail.html')
        self.assertTemplateUsed(response, 'entry/formtemplates/generic.html')
        self.assertContains(response, 
            '<input id="id_form-0-source" name="form-0-source" type="hidden" value="1" />', 
            count=1
        )
        
    def test_fixed_language_in_save(self):
        self.client.login(username="admin", password="test")
        task = Task.objects.create(
            editor=self.editor,
            name="Test Task - Fixed Language",
            description="",
            language=self.lang,
            source=self.source,
            done=False,
            view="GenericView",
            records=1, # needed so we don't have too many empty forms to validate
        )
        form_data = self.form_data.copy()
        response = self.client.post(task.get_absolute_url(), form_data, follow=True)
        
        # no errors
        assert task.lexicon.count() == 1
        self.assertRedirects(response, 
            reverse('entry:complete', kwargs={'pk': task.id}), 
            status_code=302, target_status_code=200
        )
        self.assertTemplateUsed(response, 'entry/complete.html')
        
        assert Task.objects.get(pk=task.id).done

    def test_fixed_source_in_save(self):
        self.client.login(username="admin", password="test")
        task = Task.objects.create(
            editor=self.editor,
            name="Test Task - Fixed Language",
            description="",
            language=self.lang,
            source=self.source,
            done=False,
            view="GenericView",
            records=1, # needed so we don't have too many empty forms to validate
        )
        form_data = self.form_data.copy()
        response = self.client.post(task.get_absolute_url(), form_data, follow=True)
        # no errors
        assert task.lexicon.count() == 1
        self.assertRedirects(response, 
            reverse('entry:complete', kwargs={'pk': task.id}), 
            status_code=302, target_status_code=200
        )
        self.assertTemplateUsed(response, 'entry/complete.html')
        assert Task.objects.get(pk=task.id).done

    def test_error_on_unfixed_language_in_save(self):
        self.client.login(username="admin", password="test")
        task = Task.objects.create(
            editor=self.editor,
            name="Test Task - Fixed Language",
            description="",
            source=self.source,
            done=False,
            view="GenericView",
            records=1, # needed so we don't have too many empty forms to validate
        )
        form_data = self.form_data.copy()
        form_data['form-0-language'] =  ""  # remove language

        response = self.client.post(task.get_absolute_url(), form_data)
        self.assertEqual(response.status_code, 200)
        assert response.context['formset'].errors[0] == {'language': [u'This field is required.']}
