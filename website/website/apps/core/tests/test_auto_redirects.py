from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.contrib.redirects.models import Redirect

from website.apps.core.models import Language, Source, Family, AlternateName


class RedirectionTestMixin(object):
    """Test automatic redirection on slug editing"""
    
    model = None
    slug_field = 'slug'
    
    def setUp(self):
        self.editor = User.objects.create(username='admin')
        self.language = Language.objects.create(language='A', slug='langa', 
                                             information='i.1', classification='a, b',
                                             isocode='aaa', editor=self.editor)
        self.altname = AlternateName.objects.create(language=self.language, name='x',
                                             slug='x', editor=self.editor)
        self.family = Family.objects.create(family='An', slug='s1', editor=self.editor)
        self.source = Source.objects.create(year="1991", author='Smith', 
                                    slug='Smith1991', reference='S2',
                                    comment='c1', editor=self.editor)
        self.client = Client()
    
    def _change_slugfield(self, obj, new="newslug"):
        setattr(obj, self.slug_field, new)
        obj.save()
        return obj
        
    def test_initial(self):
        if self.model is None:
            return
        obj = self.model.objects.all()[0]
        response = self.client.get(obj.get_absolute_url())
        self.assertEqual(response.status_code, 200)
    
    def test_redirect_created(self):
        assert len(Redirect.objects.all()) == 0
        
        obj = self.model.objects.all()[0]
        old_url = obj.get_absolute_url()
        self._change_slugfield(obj)
        
        assert old_url != obj.get_absolute_url()
        
        r = Redirect.objects.filter(old_path=old_url).get()
        assert r.new_path == obj.get_absolute_url()
    
    def test_request_redirects(self):
        obj = self.model.objects.all()[0]
        old_slug = obj.slug
        old_url = obj.get_absolute_url()
        
        self._change_slugfield(obj)
        
        assert obj.slug != old_slug, "Slug hasn't changed!"
        assert obj.get_absolute_url() != old_url, "URL hasn't changed!"
        
        response = self.client.get(old_url)
        self.assertRedirects(response, obj.get_absolute_url(), status_code=301, target_status_code=200)
        

class TestRedirectionLanguage(RedirectionTestMixin, TestCase):
    model = Language


class TestRedirectionSource(RedirectionTestMixin, TestCase):
    model = Source


class TestRedirectionFamily(RedirectionTestMixin, TestCase):
    model = Family

