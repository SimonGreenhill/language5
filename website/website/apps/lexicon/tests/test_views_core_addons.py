"""
Extra tests for core views with lexicon add-ons
"""
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from website.apps.lexicon.tests import DataMixin, DataMixinLexicon
from website.apps.lexicon.models import Word, WordSubset, Lexicon

class Test_SourceDetailWithLexicon(DataMixinLexicon, TestCase):
    def test_sorting(self):
        url = reverse('source-detail', kwargs={'slug': self.source1.slug})
        response = self.client.get(url, {'sort': 'entry'})
        for i, obj in enumerate([self.lexicon1, self.lexicon3]):
            assert response.context['table'].rows[i].record == obj
        response = self.client.get(url, {'sort': '-entry'})
        for i, obj in enumerate([self.lexicon3, self.lexicon1]):
            assert response.context['table'].rows[i].record == obj
    
    def test_sorting_invalid(self):
        url = reverse('source-detail', kwargs={'slug': self.source1.slug})
        response = self.client.get(url, {'sort': 'sausage'})
        for i, obj in enumerate([self.lexicon1, self.lexicon3]):
            assert response.context['table'].rows[i].record == obj


class Test_LanguageDetailWithLexicon(DataMixinLexicon, TestCase):
    def test_sorting(self):
        url = reverse('language-detail', kwargs={'language': self.lang1.slug})
        response = self.client.get(url, {'sort': 'entry'})
        for i, obj in enumerate([self.lexicon1, self.lexicon3]):
            assert response.context['table'].rows[i].record == obj
        response = self.client.get(url, {'sort': '-entry'})
        for i, obj in enumerate([self.lexicon3, self.lexicon1]):
            assert response.context['table'].rows[i].record == obj
    
    def test_sorting_invalid(self):
        url = reverse('language-detail', kwargs={'language': self.lang1.slug})
        response = self.client.get(url, {'sort': 'sausage'})
        for i, obj in enumerate([self.lexicon1, self.lexicon3]):
            assert response.context['table'].rows[i].record == obj

