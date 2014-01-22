from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from website.apps.core.models import Language, Source
from website.apps.lexicon.models import Lexicon
from website.apps.pronouns.models import Paradigm, Pronoun
from website.apps.pronouns.tests import DefaultSettingsMixin




class TestCopyParadigm(DefaultSettingsMixin, TestCase):
    
    def setUp(self):
        self.add_fixtures()
        
    def setUp(self):
        self.add_fixtures()
        self.url = reverse('pronouns:copy_paradigm', kwargs={'paradigm_id': self.pdm.id})
        self.client = Client()
        self.client.login(username='admin', password='test')
        self.response = self.client.get(self.url)
    
    def test_200ok(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'pronouns/copy.html')
    
    def test_fail_when_not_logged_in(self):
        self.assertEqual(self.client.get(self.url).status_code, 200)
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "%s?next=%s" % (reverse('login'), 
            reverse("pronouns:copy_paradigm", kwargs={'paradigm_id': self.pdm.id})))
        
    def test_request_doesnt_generate(self):
        assert Paradigm.objects.count() == 1
        self.assertTemplateUsed(self.response, 'pronouns/copy.html')
        assert Paradigm.objects.count() == 1
        
    def test_adds_paradigm(self):
        postdata = {
            'submit': 'true',
            'pdm-language': u'%d' % self.lang.id,
            'pdm-source': u'%d' % self.source.id,
        }
        response = self.client.post(self.url, postdata)
        self.assertRedirects(response, 
            reverse('pronouns:detail', kwargs={'paradigm_id': 2}))
        assert Paradigm.objects.count() == 2
        
    def test_updates_language(self):
        lang2 = Language.objects.create(language='B', 
                                         slug='langb', 
                                         information='', 
                                         classification='',
                                         isocode='bbb', 
                                         editor=self.editor)
        postdata = {
            'submit': 'true',
            'pdm-language': u'%d' % lang2.id,
            'pdm-source': u'%d' % self.source.id,
            'pdm-comment': self.pdm.comment,
        }
        response = self.client.post(self.url, postdata)
        self.assertRedirects(response, 
            reverse('pronouns:detail', kwargs={'paradigm_id': 2}))
        assert Paradigm.objects.count() == 2
        p = Paradigm.objects.get(pk=2)
        assert p.language == lang2 # CHANGED
        assert p.source == self.pdm.source
        assert p.comment == self.pdm.comment
        # check the original hasn't changed
        old_p = Paradigm.objects.get(pk=1)
        assert old_p.language == self.pdm.language != lang2
        
    def test_updates_source(self):
        source2 = Source.objects.create(year=2001, 
                                         author='Jones', 
                                         slug='Jones2001', 
                                         reference='Jones 2',
                                         comment='better than Smith!', 
                                         editor=self.editor)
        postdata = {
            'submit': 'true',
            'pdm-language': u'%d' % self.lang.id,
            'pdm-source': u'%d' % source2.id,
            'pdm-comment': self.pdm.comment,
        }
        response = self.client.post(self.url, postdata)
        self.assertRedirects(response, 
            reverse('pronouns:detail', kwargs={'paradigm_id': 2}))
        assert Paradigm.objects.count() == 2
        p = Paradigm.objects.get(pk=2)
        assert p.language == self.lang
        assert p.source == source2 # CHANGED
        assert p.comment == self.pdm.comment
        # check the original hasn't changed
        old_p = Paradigm.objects.get(pk=1)
        assert old_p.source == self.pdm.source != source2
        
    def test_updates_comment(self):
        postdata = {
            'submit': 'true',
            'pdm-language': u'%d' % self.lang.id,
            'pdm-source': u'%d' % self.source.id,
            'pdm-comment': u'Much better!'
        }
        response = self.client.post(self.url, postdata)
        self.assertRedirects(response, 
            reverse('pronouns:detail', kwargs={'paradigm_id': 2}))
        assert Paradigm.objects.count() == 2
        p = Paradigm.objects.get(pk=2)
        assert p.language == self.lang
        assert p.source == self.source
        assert p.comment == postdata['pdm-comment'] # CHANGED
        # check the original hasn't change
        old_p = Paradigm.objects.get(pk=1)
        assert old_p.comment == self.pdm.comment != postdata['pdm-comment']
    
    def test_updates_analect(self):
        postdata = {
            'submit': 'true',
            'pdm-language': u'%d' % self.lang.id,
            'pdm-source': u'%d' % self.source.id,
            'pdm-comment': self.pdm.comment,
            'pdm-analect': u'F',
        }
        response = self.client.post(self.url, postdata)
        self.assertRedirects(response, 
            reverse('pronouns:detail', kwargs={'paradigm_id': 2}))
        assert Paradigm.objects.count() == 2
        p = Paradigm.objects.get(pk=2)
        assert p.language == self.lang
        assert p.source == self.source
        assert p.comment == self.pdm.comment
        assert p.analect == u'F'
        # check the original hasn't change
        old_p = Paradigm.objects.get(pk=1)
        assert old_p.analect == self.pdm.analect != postdata['pdm-analect']
    