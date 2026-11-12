from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from website.apps.core.models import Language, Source
from website.apps.lexicon.models import Lexicon, Word


class TestSearch(TestCase):
    @classmethod
    def setUpTestData(cls):
        ed = User.objects.create_user('ed', 'ed@example.com', 'x')
        cls.hand = Word.objects.create(word='hand', slug='hand', editor=ed)
        cls.handle = Word.objects.create(word='left hand', slug='left-hand', editor=ed)
        src = Source.objects.create(author='Smith', year='1991', slug='smith1991', editor=ed)
        lang = Language.objects.create(language='Kamoro', slug='kamoro', editor=ed)
        for i in range(60):
            Lexicon.objects.create(language=lang, source=src, word=cls.hand, entry=f'hand{i}', editor=ed)

    def get(self, **params):
        return self.client.get(reverse('search'), params)

    def test_empty_query(self):
        response = self.get()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['groups'], [])

    def test_grouped_with_exact_match_first(self):
        response = self.get(q='hand')
        groups = {g['key']: g for g in response.context['groups']}
        self.assertEqual(list(groups['words']['results']), [self.hand, self.handle])
        self.assertEqual(groups['lexicon']['count'], 60)
        self.assertEqual(len(groups['lexicon']['results']), 20)  # preview only
        self.assertContains(response, 'All 60 lexical items')

    def test_type_filter_paginates(self):
        response = self.get(q='hand', type='lexicon', page=2)
        self.assertEqual([g['key'] for g in response.context['groups']], ['lexicon'])
        self.assertEqual(response.context['page_obj'].number, 2)
        self.assertEqual(len(response.context['groups'][0]['results']), 10)
        self.assertEqual(response.context['prev_url'], '?q=hand&type=lexicon&page=1')

    def test_unknown_type_shows_all(self):
        response = self.get(q='hand', type='nonsense')
        self.assertIsNone(response.context['selected'])

    def test_no_results(self):
        self.assertContains(self.get(q='zzzz'), 'No results for')

    def test_query_is_url_encoded(self):
        response = self.get(q='hand & foot')
        self.assertEqual(response.context['all_url'], '?q=hand+%26+foot')
