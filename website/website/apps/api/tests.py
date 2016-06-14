from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from website.apps.core.models import Source, Language, Family, AlternateName, Location
from website.apps.lexicon.tests import DataMixin

# "language": {"list_endpoint": "/api/v1/language/",
# "languagemap": {"list_endpoint": "/api/v1/languagemap/", 
# "lexicon": {"list_endpoint": "/api/v1/lexicon/", 
# "source": {"list_endpoint": "/api/v1/source/", 
# "word": {"list_endpoint": "/api/v1/word/",

# TODO: test /api redirects to /api/v1


class Test_LanguageResource(DataMixin, TestCase):
    
    url = '/api/v1/language/'
    
    def setUp(self):
        self.response = self.client.get(self.url)
        self.json = self.response.json()
    
    def test_200ok(self):
        self.assertEqual(self.response.status_code, 200)
        
    def test_result(self):
        assert len(self.json['objects']) == 2
        records = [o['slug'] for o in self.json['objects']]
        assert 'langa' in records
        assert 'langb' in records
        
    
class Test_SourceResource(DataMixin, TestCase):

    url = '/api/v1/source/'
    
    def setUp(self):
        self.response = self.client.get(self.url)
        self.json = self.response.json()
    
    def test_200ok(self):
        self.assertEqual(self.response.status_code, 200)
        
    def test_result(self):
        assert len(self.json['objects']) == 2
        records = [o['slug'] for o in self.json['objects']]
        assert 'Jones2002' in records
        assert 'Smith1991' in records


class Test_WordResource(DataMixin, TestCase):

    url = '/api/v1/word/'
    
    def setUp(self):
        self.response = self.client.get(self.url)
        self.json = self.response.json()
    
    def test_200ok(self):
        self.assertEqual(self.response.status_code, 200)
        
    def test_result(self):
        assert len(self.json['objects']) == 3
        records = [o['slug'] for o in self.json['objects']]
        assert 'hand' in records
        assert 'one' in records
        assert 'two' in records


class Test_LexiconResource(DataMixin, TestCase):
    
    url = '/api/v1/lexicon/'
    
    def setUp(self):
        self.response = self.client.get(self.url)
        self.json = self.response.json()
    
    def test_200ok(self):
        self.assertEqual(self.response.status_code, 200)
        
    def test_result(self):
        assert len(self.json['objects']) == 3
        records = [o['entry'] for o in self.json['objects']]
        assert 'A' in records
        assert 'B' in records
        assert 'C' in records


class Test_LanguageMapResource(DataMixin, TestCase):
    url = '/api/v1/languagemap/'
    
    def setUp(self):
        self.loc1 = Location.objects.create(
            isocode=self.lang1.isocode,
            latitude=1.0,
            longitude=-5.6,
            editor=self.editor
        )
        self.loc2 = Location.objects.create(
            isocode=self.lang2.isocode,
            latitude=-20.0,
            longitude=100.1,
            editor=self.editor
        )
        self.response = self.client.get(self.url)
        self.json = self.response.json()
    
    def test_200ok(self):
        self.assertEqual(self.response.status_code, 200)
        
    def test_result(self):
        assert len(self.json['objects']) == 2
        records = [o['language'] for o in self.json['objects']]
        assert 'A' in records
        assert 'B' in records
