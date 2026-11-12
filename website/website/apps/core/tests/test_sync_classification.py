import csv
import tempfile
from io import StringIO
from pathlib import Path

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
from reversion.models import Version

from website.apps.core.models import Language

LANGUAGES = [
    # ID, Name, Level, Language_ID
    ('fama1234', 'Family A', 'family', ''),
    ('subb1234', 'Sub B', 'family', ''),
    ('lang1234', 'Lang One', 'language', ''),
    ('dial1234', 'Dialect One', 'dialect', 'lang1234'),
    ('isol1234', 'Isolate X', 'language', ''),
    ('isod1234', 'Isolate X Dialect', 'dialect', 'isol1234'),
]
CLASSIFICATION = {
    'subb1234': 'fama1234',
    'lang1234': 'fama1234/subb1234',
    'dial1234': 'fama1234/subb1234/lang1234',
    'isol1234': '',
    'isod1234': 'isol1234',
}


class TestSyncClassification(TestCase):
    @classmethod
    def setUpTestData(cls):
        ed = User.objects.create_user('admin', 'a@b.c', 'x')
        mk = lambda slug, gc, cl: Language.objects.create(
            language=slug, slug=slug, glottocode=gc, classification=cl, editor=ed)
        cls.lang = mk('lang', 'lang1234', 'Old, Path')
        cls.dial = mk('dial', 'dial1234', '')
        cls.isol = mk('isol', 'isol1234', 'Language isolate')
        cls.isod = mk('isod', 'isod1234', '')
        cls.same = mk('same', 'lang1234', 'Family A, Sub B')
        cls.proto = mk('proto', 'subb1234', 'Old')
        cls.proto_top = mk('proto-top', 'fama1234', '')
        cls.nocode = mk('nocode', None, 'Keep Me')
        cls.unknown = mk('unknown', 'zzzz9999', 'Keep Me Too')

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
                w.writerow([f'{gc}-level', gc, 'level', 'x'])

    def tearDown(self):
        self.tmp.cleanup()

    def run_cmd(self, *args):
        out = StringIO()
        call_command('sync_classification', self.tmp.name, *args, stdout=out)
        return out.getvalue()

    def classif(self, obj):
        obj.refresh_from_db()
        return obj.classification

    def test_dry_run_reports_without_saving(self):
        out = self.run_cmd()
        self.assertIn('Old, Path', out)
        self.assertIn('Family A, Sub B', out)
        self.assertIn('zzzz9999', out)
        self.assertIn('nocode', out)
        self.assertNotIn('same', out.split('Skipped')[0])  # unchanged rows not listed as changes
        self.assertEqual(self.classif(self.lang), 'Old, Path')

    def test_apply(self):
        self.run_cmd('--apply')
        self.assertEqual(self.classif(self.lang), 'Family A, Sub B')
        self.assertEqual(self.classif(self.dial), 'Family A, Sub B')  # language ancestor dropped
        self.assertEqual(self.classif(self.isol), 'Isolate X')
        self.assertEqual(self.classif(self.isod), 'Isolate X')
        self.assertEqual(self.classif(self.same), 'Family A, Sub B')
        self.assertEqual(self.classif(self.proto), 'Family A, Sub B')  # family code includes itself
        self.assertEqual(self.classif(self.proto_top), 'Family A')
        self.assertEqual(self.classif(self.nocode), 'Keep Me')
        self.assertEqual(self.classif(self.unknown), 'Keep Me Too')

    def test_apply_records_history(self):
        self.run_cmd('--apply')
        self.assertEqual(Version.objects.get_for_object(self.lang).count(), 1)
        self.assertEqual(Version.objects.get_for_object(self.same).count(), 0)
