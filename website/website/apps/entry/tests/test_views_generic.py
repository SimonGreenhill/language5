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


class Test_GenericViewBase(DataMixin):
    """Tests the GenericView Detail Page -- base things"""

    def test_testimage_is_present(self):
        """
        This test makes sure that the test image is present on the file-system
        """
        from os.path import join, isfile
        from django.conf import settings
        test_file = join(settings.MEDIA_ROOT, self.file_testimage)
        assert isfile(test_file), \
            """Missing Test Image File on File-System at %s! Other tests will fail!""" % test_file
        
    def test_error_when_not_logged_in(self):
        response = self.client.get(self.task.get_absolute_url())
        self.assertEqual(response.status_code, 302) 
        self.assertRedirects(response, 
             "/accounts/login/?next=%s" % self.task.get_absolute_url(), 
             status_code=302, target_status_code=200
        )

    def test_ok_when_logged_in(self):
        self.client.login(username="admin", password="test")
        response = self.client.get(self.task.get_absolute_url())
        self.assertEqual(response.status_code, 200)


class Test_GenericView(DataMixin):
    """Tests the GenericView Detail Page"""
    
    def setUp(self):
        self.client.login(username="admin", password="test")
    
    # helper
    def _make_task(self, name="", done=False, records=1):
        return Task.objects.create(
            editor=self.editor,
            name=name,
            image=self.file_testimage,
            description="",
            source=self.source,
            language=self.lang,
            done=done,
            completable=False,
            view="GenericView",
            records=records
        )
    
    def test_template_used(self):
        response = self.client.get(self.task.get_absolute_url())
        self.assertTemplateUsed(response, 'entry/detail.html')
        
    def test_active_task(self):
        response = self.client.get(self.task.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        
    def test_completed_task(self):
        task = self._make_task(done=True)
        response = self.client.get(task.get_absolute_url())
        self.assertRedirects(response, 
            reverse('entry:complete', kwargs={'pk': task.id}), 
            status_code=302, target_status_code=200
        )
        
    def test_number_of_records(self):
        response = self.client.get(self.task.get_absolute_url())
        assert len(response.context['formset'].forms) == 1
        task = self._make_task(records=2)
        response = self.client.get(task.get_absolute_url())
        assert len(response.context['formset'].forms) == 2
        
    def test_post_does_not_set_done_if_not_completable(self):
        task = self._make_task()
        response = self.client.post(task.get_absolute_url(), self.form_data)
        assert not Task.objects.get(pk=task.id).done
    
    def test_post_sets_done_if_completable(self):
        task = self._make_task()
        task.completable = True
        task.save()
        response = self.client.post(task.get_absolute_url(), self.form_data)
        assert Task.objects.get(pk=task.id).done
    
    def test_unfixed_language_in_template(self):
        task = self._make_task()
        task.language = None
        task.save()
        
        response = self.client.get(task.get_absolute_url())
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entry/detail.html')
        self.assertTemplateUsed(response, 'entry/formtemplates/generic.html')
        self.assertContains(
            response,
            '<option value="%d">%s</option>' % (self.lang.id, self.lang.language),
            count=1
        )
        self.assertContains(response, 'form-0-language', count=3)
        
    def test_fixed_language_in_template(self):
        L = Language.objects.create(
            language='X',
            slug='another-language',
            editor=self.editor
        )
        
        task = self._make_task()
        task.language = L
        task.save()
        
        response = self.client.get(task.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entry/detail.html')
        self.assertTemplateUsed(response, 'entry/formtemplates/generic.html')
        self.assertContains(response, 
            '<input id="id_form-0-language" name="form-0-language" type="hidden" value="%d" />' % L.id,
            count=1
        )
    
    def test_fixed_source_in_template(self):
        
        S = Source.objects.create(
            year="xxxx",
            author='TEST SOURCE',
            slug='another-test-source',
            editor=self.editor
        )
        task = self._make_task()
        task.source = S
        task.save()
        
        response = self.client.get(task.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entry/detail.html')
        self.assertTemplateUsed(response, 'entry/formtemplates/generic.html')
        self.assertContains(response, 
            '<input id="id_form-0-source" name="form-0-source" type="hidden" value="%d" />' % S.id,
            count=1
        )
        
    def test_error_on_unfixed_language_in_save(self):
        task = self._make_task()
        task.language = None
        task.save()
        
        form_data = self.form_data.copy()
        form_data['form-0-language'] =  ""  # remove language
        
        response = self.client.post(task.get_absolute_url(), form_data)
        self.assertEqual(response.status_code, 200)
        assert response.context['formset'].errors[0] == {'language': [u'This field is required.']}
    
