from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from website.apps.core.models import Source
from website.apps.cognacy.tests.data import DataMixin


class Test_CognateSourceIndex(DataMixin, TestCase):
    def setUp(self):
        super(Test_CognateSourceIndex, self).setUp()
        self.url = reverse('cognacy:source_index')
        self.empty_source = Source.objects.create(
            year="1992", author='Greenhill', 
            slug='greenhill1992', reference='',
            comment='', editor=self.editor
        )
    
    def test_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'cognacy/index.html')
    
    def test_get_data(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        data = response.context['table'].data.data
        assert len(data) == 1
        assert data[0] == self.source
        assert self.empty_source not in data
    
    def test_count(self):
        # source should have count=2
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        data = response.context['table'].data.data
        assert data[0].count == 2