import csv
import tempfile
from io import StringIO
from pathlib import Path

from django.contrib.auth.models import User
from django.contrib.redirects.models import Redirect
from django.core.management import call_command
from django.test import TestCase

from website.apps.core.models import Family, Language

LANGUAGES = [
    # ID, Name, Level, Language_ID
    ('fama1234', 'Family A', 'family', ''),
    ('suba1234', 'Sub A', 'family', ''),
    ('lana1234', 'Lang A', 'language', ''),
    ('lanb1234', 'Lang B', 'language', ''),
    ('famb1234', 'Family B', 'family', ''),
    ('lanc1234', 'Lang C', 'language', ''),
    ('isol1234', 'Isolate X', 'language', ''),
    ('isod1234', 'Isolate X Dialect', 'dialect', 'isol1234'),
]
CLASSIFICATION = {
    'suba1234': 'fama1234',
    'lana1234': 'fama1234/suba1234',
    'lanb1234': 'fama1234',
    'lanc1234': 'famb1234',
    'isol1234': '',
    'isod1234': 'isol1234',
}


class TestSyncFamilies(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.ed = User.objects.create_superuser('admin', 'a@b.c', 'x')
        fam = lambda slug: Family.objects.create(family=slug.title(), slug=slug, editor=cls.ed)
        cls.big, cls.dup, cls.empty = fam('big'), fam('dup'), fam('empty')
        lang = lambda slug, gc, *fams: Language.objects.create(
            language=slug, slug=slug, glottocode=gc, editor=cls.ed).family.set(fams)
        lang('a1', 'lana1234', cls.big, cls.dup)
        lang('a2', 'lanb1234', cls.big)
        lang('c1', 'lanc1234', cls.big)
        lang('x1', 'isod1234', cls.dup)
        lang('nocode', None, cls.big)

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        d = Path(self.tmp.name)
        with open(d / 'languages.csv', 'w', newline='') as f:
            w = csv.writer(f)
            w.writerow(['ID', 'Name', 'Level', 'Language_ID'])
            w.writerows(LANGUAGES)
        with open(d / 'values.csv', 'w', newline='') as f:
            w = csv.writer(f)
            w.writerow(['ID', 'Language_ID', 'Parameter_ID', 'Value'])
            for gc, path in CLASSIFICATION.items():
                w.writerow([f'{gc}-classification', gc, 'classification', path])

    def tearDown(self):
        self.tmp.cleanup()

    def run_cmd(self, *args):
        out = StringIO()
        call_command('sync_families', self.tmp.name, *args, stdout=out)
        return out.getvalue()

    def families(self, slug):
        return sorted(Language.objects.get(slug=slug).family.values_list('slug', flat=True))

    def test_dry_run_changes_nothing(self):
        out = self.run_cmd()
        self.assertIn('big -> family-a', out)
        self.assertEqual(self.families('a1'), ['big', 'dup'])
        self.assertFalse(Redirect.objects.exists())

    def test_apply(self):
        self.run_cmd('--apply')
        self.assertEqual(self.families('a1'), ['family-a'])
        self.assertEqual(self.families('a2'), ['family-a'])
        self.assertEqual(self.families('c1'), ['family-b'])
        self.assertEqual(self.families('x1'), ['isolate-x'])  # dialect of an isolate
        self.assertEqual(self.families('nocode'), [])
        # big is renamed in place (keeps its row), dup takes the isolate, empty is deleted
        self.assertEqual(Family.objects.get(pk=self.big.pk).glottocode, 'fama1234')
        self.assertEqual(Family.objects.get(pk=self.dup.pk).slug, 'isolate-x')
        self.assertFalse(Family.objects.filter(slug='empty').exists())
        self.assertEqual(
            sorted(Family.objects.values_list('slug', 'family', 'glottocode')),
            [('family-a', 'Family A', 'fama1234'), ('family-b', 'Family B', 'famb1234'),
             ('isolate-x', 'Isolate X', 'isol1234')])

    def test_redirects(self):
        self.run_cmd('--apply')
        redirects = dict(Redirect.objects.values_list('old_path', 'new_path'))
        self.assertEqual(redirects['/family/big'], '/family/family-a')
        self.assertEqual(redirects['/family/dup'], '/family/isolate-x')
        self.assertEqual(redirects['/family/empty'], '/family/')
        self.assertEqual(self.client.get('/family/big').status_code, 301)

    def test_drop(self):
        out = self.run_cmd('--apply', '--drop', 'dup')
        self.assertIn('delete\tdup\t404', out)
        self.assertFalse(Family.objects.filter(pk=self.dup.pk).exists())
        self.assertEqual(self.families('x1'), ['isolate-x'])  # created fresh instead
        self.assertFalse(Redirect.objects.filter(old_path='/family/dup').exists())
        self.assertEqual(self.client.get('/family/dup').status_code, 404)

    def test_deleted_family_redirects_to_largest_successor(self):
        # a second family competing for Family A loses and is deleted
        loser = Family.objects.create(family='Loser', slug='loser', editor=self.ed)
        Language.objects.get(slug='a2').family.add(loser)
        self.run_cmd('--apply')
        self.assertFalse(Family.objects.filter(slug='loser').exists())
        self.assertEqual(Redirect.objects.get(old_path='/family/loser').new_path, '/family/family-a')

    def test_stores_glottolog_tree(self):
        self.run_cmd('--apply')
        self.assertEqual(Family.objects.get(slug='family-a').glottolog_tree, {
            'fama1234': ['Family A', 'family', None],
            'suba1234': ['Sub A', 'family', 'fama1234'],
            'lana1234': ['Lang A', 'language', 'suba1234'],
            'lanb1234': ['Lang B', 'language', 'fama1234'],
        })
        self.assertEqual(Family.objects.get(slug='isolate-x').glottolog_tree, {
            'isol1234': ['Isolate X', 'language', None],
            'isod1234': ['Isolate X Dialect', 'dialect', 'isol1234'],
        })

    def test_rerun_is_noop(self):
        self.run_cmd('--apply')
        out = self.run_cmd('--apply')
        self.assertIn('0 renamed, 0 created, 0 deleted, 0 languages changed', out)
