# -*- coding: utf-8 -*-
"""
Tests for the crawler-trap mitigation (see fix.md / crawler_trap.py).

NOTE: these were written against the project's existing test conventions but
could not be executed in the authoring environment (no Django 1.11 / Py2 runtime
available). Run with:  ./manage.py test website.apps.core.tests.test_crawler_trap
"""
from django.test import TestCase
from django.test.client import Client, RequestFactory
from django.http import Http404, HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse

from website.apps.core.models import Language
from website.apps.core.tables import LanguageIndexTable
from website.apps.core.crawler_trap import (
    MAX_PAGE, valid_sort_columns, canonical_sort_redirect, guard_page,
    list_seo_context,
)


class Test_valid_sort_columns(TestCase):
    def test_real_columns_present(self):
        cols = valid_sort_columns(LanguageIndexTable)
        self.assertIn('language', cols)
        self.assertIn('isocode', cols)

    def test_junk_absent(self):
        self.assertNotIn('sausage', valid_sort_columns(LanguageIndexTable))


class Test_guard_page(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def _get(self, query):
        return self.factory.get('/language/', query)

    def test_absent_page_ok(self):
        self.assertIsNone(guard_page(self._get({})))

    def test_valid_page_ok(self):
        self.assertIsNone(guard_page(self._get({'page': '3'})))

    def test_non_integer_404(self):
        with self.assertRaises(Http404):
            guard_page(self._get({'page': 'banana'}))

    def test_zero_404(self):
        with self.assertRaises(Http404):
            guard_page(self._get({'page': '0'}))

    def test_negative_404(self):
        with self.assertRaises(Http404):
            guard_page(self._get({'page': '-5'}))

    def test_absurdly_large_404(self):
        with self.assertRaises(Http404):
            guard_page(self._get({'page': str(MAX_PAGE + 1)}))


class Test_canonical_sort_redirect(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def _get(self, query):
        return self.factory.get('/language/', query)

    def test_absent_sort_passes(self):
        self.assertIsNone(canonical_sort_redirect(self._get({}), LanguageIndexTable))

    def test_valid_sort_passes(self):
        self.assertIsNone(
            canonical_sort_redirect(self._get({'sort': 'language'}), LanguageIndexTable)
        )

    def test_valid_descending_sort_passes(self):
        self.assertIsNone(
            canonical_sort_redirect(self._get({'sort': '-language'}), LanguageIndexTable)
        )

    def test_invalid_sort_redirects(self):
        response = canonical_sort_redirect(
            self._get({'sort': 'sausage'}), LanguageIndexTable
        )
        self.assertIsInstance(response, HttpResponsePermanentRedirect)
        self.assertEqual(response['Location'], '/language/')

    def test_invalid_sort_preserves_other_params(self):
        response = canonical_sort_redirect(
            self._get({'sort': 'sausage', 'subset': 'A'}), LanguageIndexTable
        )
        self.assertIn('subset=A', response['Location'])
        self.assertNotIn('sort=', response['Location'])


class Test_list_seo_context(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def _ctx(self, query):
        return list_seo_context(self.factory.get('/language/', query))

    def test_clean_page_is_indexable(self):
        ctx = self._ctx({})
        self.assertFalse(ctx['noindex'])
        self.assertTrue(ctx['canonical_url'].endswith('/language/'))

    def test_sorted_page_is_noindex(self):
        self.assertTrue(self._ctx({'sort': 'language'})['noindex'])

    def test_deep_page_is_noindex(self):
        self.assertTrue(self._ctx({'page': '2'})['noindex'])

    def test_first_page_is_indexable(self):
        self.assertFalse(self._ctx({'page': '1'})['noindex'])

    def test_canonical_strips_sort_and_page(self):
        canonical = self._ctx({'sort': 'language', 'page': '2'})['canonical_url']
        self.assertTrue(canonical.endswith('/language/'))

    def test_canonical_keeps_subset(self):
        canonical = self._ctx({'subset': 'A', 'sort': 'language'})['canonical_url']
        self.assertIn('subset=A', canonical)


class Test_LanguageIndex_CrawlerTrap(TestCase):
    """End-to-end behaviour on a real list view."""

    @classmethod
    def setUpTestData(cls):
        from django.contrib.auth.models import User
        editor = User.objects.create_user('admin', 'a@b.com', 'test')
        Language.objects.create(
            language='Language1', slug='language1', information='',
            classification='', isocode='aaa', editor=editor
        )

    def setUp(self):
        self.client = Client()
        self.url = reverse('language-index')

    def test_valid_sort_200(self):
        self.assertEqual(self.client.get(self.url + '?sort=language').status_code, 200)

    def test_invalid_sort_301(self):
        response = self.client.get(self.url + '?sort=sausage')
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response['Location'], self.url)

    def test_bogus_page_word_404(self):
        self.assertEqual(self.client.get(self.url + '?page=banana').status_code, 404)

    def test_bogus_page_huge_404(self):
        self.assertEqual(self.client.get(self.url + '?page=999999').status_code, 404)

    def test_noindex_meta_on_sorted_page(self):
        response = self.client.get(self.url + '?sort=language')
        self.assertContains(response, 'noindex')

    def test_canonical_on_clean_page(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'rel="canonical"')
        self.assertNotContains(response, 'noindex')
