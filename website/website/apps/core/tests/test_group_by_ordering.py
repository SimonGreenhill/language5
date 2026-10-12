"""Django 3.1+ ignores Meta.ordering on GROUP BY queries; annotate() querysets must order explicitly."""
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from website.apps.core.models import Family, Language, Location, Source
from website.apps.lexicon.models import Cognate, CognateSet, Lexicon, Word


class TestGroupByOrdering(TestCase):
    @classmethod
    def setUpTestData(cls):
        ed = User.objects.create_user('ed', 'ed@example.com', 'test')
        word = Word.objects.create(word='Hand', slug='hand', editor=ed)
        # created in reverse so insertion order != alphabetical order
        for name in ('Zeta', 'Muon', 'Alpha'):
            fam = Family.objects.create(family=name, slug=name.lower(), editor=ed)
            src = Source.objects.create(author=name, year='2000', slug=name.lower(), editor=ed)
            lang = Language.objects.create(language=name, slug=name.lower(), isocode=name[:3].lower(), editor=ed)
            lang.family.add(fam)
            Location.objects.create(isocode=lang.isocode, latitude=0, longitude=0, editor=ed)
            lex = Lexicon.objects.create(language=lang, source=src, word=word, entry='x', editor=ed)
            cs = CognateSet.objects.create(protoform=name, editor=ed)
            Cognate.objects.create(lexicon=lex, cognateset=cs, source=src, editor=ed)

    def test_cognacy_index(self):
        rows = self.client.get(reverse('cognacy:index')).context['table'].page.object_list
        self.assertEqual([r.record.author for r in rows], ['Alpha', 'Muon', 'Zeta'])

    def test_languagemap_api(self):
        data = self.client.get('/api/v1/languagemap/').json()['objects']
        self.assertEqual([o['language'] for o in data], ['Alpha', 'Muon', 'Zeta'])

    def test_family_chart(self):
        from website.apps.statistics.views import make_family_chart
        self.assertEqual(make_family_chart()['data']['x'], ['Alpha', 'Muon', 'Zeta'])
