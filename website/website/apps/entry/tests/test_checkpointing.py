# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test.client import Client

from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
from website.apps.core.models import Source, Language
from website.apps.lexicon.models import Word, Lexicon
from website.apps.entry.models import Task
from website.apps.entry.dataentry import available_views
from website.apps.entry.views import encode_checkpoint, decode_checkpoint

from website.apps.entry.tests import DataMixin

class Test_Checkpointing(DataMixin):
    """Tests the Detail Page's Checkpointing"""
    @classmethod
    def setUpTestData(cls):
        super(Test_Checkpointing, cls).setUpTestData()
        # need an incomplete entry, or else we get marked as complete.
        del(cls.form_data['form-0-entry'])
    
    def test_checkpoint(self):
        task = Task.objects.create(
            editor=self.editor,
            name="Test Task",
            description="A Test of Data Entry",
            source=self.source,
            image=self.file_testimage,
            language=self.lang,
            done=False,
            checkpoint=encode_checkpoint(self.form_data),
            view="GenericView",
            records=1, # needed so we don't have too many empty forms to validate
        )
        # get from db.
        t = Task.objects.get(pk=task.id)
        assert t.checkpoint is not None
        restored = decode_checkpoint(t.checkpoint)
        for k, v in self.form_data.items():
            assert k in restored, "Missing %s from checkpoint" % k
            assert restored[k] == v, "Expected %s to be %s" % (k, v)
    
    def test_checkpoint_in_view(self):
        """Test checkpoint data goes through to view"""
        self.client.login(username="admin", password="test")
        assert self.task.checkpoint is None
        
        del(self.form_data['form-0-language']) # make form invalid
        self.form_data['form-0-entry'] = 'banana'
        response = self.client.post(self.task.get_absolute_url(), self.form_data)
        
        # now check formdata in response
        formdata = [f.clean() for f in response.context['formset'].forms]
        assert 'entry' in formdata[0]
        assert formdata[0]['entry'] == 'banana'
        
    def test_no_checkpoint_on_GET(self):
        """GET shouldn't set checkpoint"""
        self.client.login(username="admin", password="test")
        assert self.task.checkpoint is None
        response = self.client.get(self.task.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        assert self.task.checkpoint is None
        
    def test_checkpoint_on_POST(self):
        self.client.login(username="admin", password="test")
        assert self.task.checkpoint is None
        response = self.client.post(self.task.get_absolute_url(), self.form_data)
        self.assertEqual(response.status_code, 200)
        t = Task.objects.get(pk=self.task.id)
        assert t.checkpoint is not None
        
    def test_checkpoint_doesnt_override_better(self):
        """Don't restore a checkpoint if we've got a new one coming in via POST"""
        self.client.login(username="admin", password="test")
        assert self.task.checkpoint is None
        response = self.client.post(self.task.get_absolute_url(), self.form_data)
        # make sure the response has annotation = comment
        form = response.context['formset'].forms[0].data['form-0-annotation'] == u'comment'
        
        # make sure we've saved something...
        assert Task.objects.get(pk=self.task.id).checkpoint is not None
        
        # change the post data
        form_data = self.form_data.copy()
        form_data['form-0-annotation'] = 'TWO'
        response = self.client.post(self.task.get_absolute_url(), form_data)
        # Make sure - response contains annotation = 'TWO' not 'comment'
        form = response.context['formset'].forms[0].data['form-0-annotation'] == u'TWO'
        
    def test_checkpoint_with_unicode(self):
        unicode_sample = u'àáâãäåạɐæʌèéêëɛəìííîïɨịñŋòóôõöøðɔþùúûüụųʔřɬɤƀꝑšʷᵘ·'
        retrieved = decode_checkpoint(encode_checkpoint(unicode_sample))
        assert unicode_sample == retrieved
    
    def test_checkpoint_with_unicode_via_database(self):
        unicode_sample = u'àáâãäåạɐæʌèéêëɛəìííîïɨịñŋòóôõöøðɔþùúûüụųʔřɬɤƀꝑšʷᵘ·'
        task = Task.objects.create(
            editor=self.editor,
            name="Test Task",
            description="A Test of Data Entry",
            source=self.source,
            image=self.file_testimage,
            language=self.lang,
            done=False,
            checkpoint=encode_checkpoint(unicode_sample),
            view="GenericView",
            records=1, # needed so we don't have too many empty forms to validate
        )
        assert unicode_sample == decode_checkpoint(Task.objects.get(pk=task.id).checkpoint)
    
    def test_refresh_sets_checkpoint(self):
        self.client.login(username="admin", password="test")
        assert self.task.checkpoint is None
        response = self.client.post(self.task.get_absolute_url(), self.form_data)
        self.assertEqual(response.status_code, 200)
        t = Task.objects.get(pk=self.task.id)
        assert t.checkpoint is not None

