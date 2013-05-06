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
            'form-INITIAL_FORMS': u'1',
            'form-MAX_NUM_FORMS': u'1000',
            'form-0-language': self.lang.id,
            'form-0-source': self.source.id,
            'form-0-word': self.word.id,
            'form-0-entry': 'simon',
            'form-0-annotation': 'comment',
            'submit': 'true',
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


class Test_Detail_Checkpointing(TestCase):
    """Tests the Detail Page's Checkpointing"""
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
            'form-INITIAL_FORMS': u'1',
            'form-MAX_NUM_FORMS': u'1000',
            'form-0-language': self.lang.id,
            'form-0-source': self.source.id,
            'form-0-word': self.word.id,
            # need an incomplete entry, or else we get marked as complete.
            ## 'form-0-entry': 'simon',
            'form-0-annotation': 'comment',
            'submit': 'true',
        }
    
    def test_checkpoint(self):
        self.task.checkpoint = encode_checkpoint(self.form_data)
        self.task.save()
        # get from db.
        t = Task.objects.get(pk=self.task.id)
        assert t.checkpoint is not None
        restored = decode_checkpoint(t.checkpoint)
        for k, v in self.form_data.items():
            assert k in restored, "Missing %s from checkpoint" % k
            assert restored[k] == v, "Expected %s to be %s" % (k, v)
        
    def test_no_checkpoint_on_GET(self):
        """GET shouldn't set checkpoint"""
        self.client.login(username="admin", password="test")
        assert self.task.checkpoint is None
        response = self.client.get(self.task.get_absolute_url())
        self.failUnlessEqual(response.status_code, 200)
        assert self.task.checkpoint is None
        
    def test_checkpoint_on_POST(self):
        self.client.login(username="admin", password="test")
        assert self.task.checkpoint is None
        response = self.client.post(self.task.get_absolute_url(), self.form_data)
        self.failUnlessEqual(response.status_code, 200)
        t = Task.objects.get(pk=self.task.id)
        assert t.checkpoint is not None
        
    def test_checkpoint_handles_garbage(self):
        """Ensure that we don't choke if checkpoint is garbage"""
        self.task.checkpoint = "fudge"
        self.task.save()
        assert self.task.checkpoint is not None
        assert decode_checkpoint(self.task.checkpoint) is None
    
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
        self.task.checkpoint = encode_checkpoint(unicode_sample)
        self.task.save()
        assert unicode_sample == decode_checkpoint(Task.objects.get(pk=self.task.id).checkpoint)
    
    def test_refresh_sets_checkpoint(self):
        self.client.login(username="admin", password="test")
        assert self.task.checkpoint is None
        response = self.client.post(self.task.get_absolute_url(), self.form_data)
        self.failUnlessEqual(response.status_code, 200)
        t = Task.objects.get(pk=self.task.id)
        assert t.checkpoint is not None
