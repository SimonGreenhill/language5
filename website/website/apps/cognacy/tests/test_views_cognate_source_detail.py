from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from website.apps.core.models import Source
from website.apps.cognacy.tests.data import DataMixin

from website.apps.core.tests.utils import PaginatorTestMixin

class Test_CognateSourceDetail(DataMixin, PaginatorTestMixin, TestCase):
    def setUp(self):
        super(Test_CognateSourceDetail, self).setUp()
        self.url = reverse('cognacy:cognatesource_detail', kwargs={'slug': self.source.slug})
        self.empty_source = Source.objects.create(
            year="1992", author='Greenhill', 
            slug='greenhill1992', reference='',
            comment='', editor=self.editor
        )
    
    def test_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'cognacy/detail.html')
    
    def test_get_data(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        # should have two cognate sets -- 1 & 2
        assert len(response.context['table'].data.data) == 2
        assert self.cog_1_a in response.context['table'].data.data
        assert self.cog_2_b in response.context['table'].data.data
    
    def test_content(self):
        response = self.client.get(self.url)
        td = '<td class="lexicon">%s</td>'
        #print(response.content)
        assert td % self.cog_1_a.lexicon.entry in response.content.decode('utf8')
        assert td % self.cog_2_b.lexicon.entry in response.content.decode('utf8')
        assert td % self.cog_2_c.lexicon.entry not in response.content.decode('utf8')
    
    def test_empty_source(self):
        url = reverse('cognacy:cognatesource_detail', kwargs={'slug': self.empty_source.slug})
        response = self.client.get(url)
        data = response.context['table'].data.data
        assert len(data) == 0
