"""
Browser tests for the JavaScript-dependent pages (keypad, formsets, select2,
cognacy save, maps, charts, copy buttons). They guard the front-end rewrite.

Needs `pip install -r requirements.txt -r requirements-dev.txt && playwright install chromium`.
Skipped when Playwright isn't installed. Run only these: `manage.py test --tag browser`.
"""
import os
from unittest import skipUnless

from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import Client, tag
from django.urls import reverse

from website.apps.core.models import Language, Location, Source
from website.apps.entry.models import Task
from website.apps.lexicon.models import Cognate, CognateSet, Lexicon, Word

try:
    from playwright.sync_api import sync_playwright
except ImportError:  # pragma: no cover
    sync_playwright = None

def png(width, height):
    """A solid grey PNG of the given size (stdlib only)."""
    import struct, zlib
    def chunk(kind, data):
        return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data))
    rows = b''.join(b'\x00' + b'\x88' * width for _ in range(height))
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 0, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(rows)) + chunk(b'IEND', b''))


# Playwright's sync API runs an event loop; the live server's ORM calls are still synchronous.
os.environ.setdefault('DJANGO_ALLOW_ASYNC_UNSAFE', 'true')


@tag('browser')
@skipUnless(sync_playwright, 'playwright not installed')
class BrowserTestCase(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()
        super().tearDownClass()

    def setUp(self):
        self.editor = User.objects.create_superuser('admin', 'admin@example.com', 'test')
        self.lang = Language.objects.create(language='Kuman', slug='kuman', isocode='kue', editor=self.editor)
        self.source = Source.objects.create(author='Trefry', year='1969', slug='trefry1969', editor=self.editor)
        self.word = Word.objects.create(word='Hand', slug='hand', editor=self.editor)
        self.lex1 = Lexicon.objects.create(language=self.lang, source=self.source, word=self.word, entry='ku', editor=self.editor)
        self.lex2 = Lexicon.objects.create(language=self.lang, source=self.source, word=self.word, entry='kan', editor=self.editor)
        Location.objects.create(isocode='kue', latitude=-6.0, longitude=145.0, editor=self.editor)

        self.context = self.browser.new_context(permissions=['clipboard-read', 'clipboard-write'])
        # keep tests offline and deterministic: drop anything not served by the live server
        self.context.route('**/*', lambda route: route.continue_()
                           if route.request.url.startswith(self.live_server_url) else route.abort())
        self.page = self.context.new_page()
        self.errors = []
        self.page.on('pageerror', lambda e: self.errors.append(str(e)))

    def tearDown(self):
        self.context.close()

    def select2(self, select_css, text):
        """Pick an option through the select2 widget attached to `select_css`."""
        self.page.click(f'{select_css} + .select2-container')
        self.page.fill('.select2-container--open .select2-search__field', text)
        self.page.wait_for_selector('.select2-results__option--highlighted')
        self.page.keyboard.press('Enter')

    def login(self):
        client = Client()
        client.force_login(self.editor)
        self.context.add_cookies([{
            'name': 'sessionid', 'value': client.cookies['sessionid'].value,
            'url': self.live_server_url,
        }])

    def open(self, path):
        self.page.goto(self.live_server_url + path)
        self.page.wait_for_load_state('networkidle')

    def assertNoJSErrors(self):
        self.assertEqual(self.errors, [], 'JavaScript errors on page')


class TestLogin(BrowserTestCase):
    def test_login_form(self):
        self.open(reverse('login'))
        self.page.fill('input[name=username]', 'admin')
        self.page.fill('input[name=password]', 'test')
        self.page.click('input[type=submit]')
        self.page.wait_for_load_state('networkidle')
        self.assertIn('logged-in', self.page.url)
        self.assertNoJSErrors()


class TestLexiconEdit(BrowserTestCase):
    def test_keypad_inserts_character_and_saves(self):
        self.login()
        self.open(reverse('lexicon-edit', kwargs={'pk': self.lex1.pk}))
        entry = self.page.locator('input[name=entry]')
        entry.fill('ku')
        entry.focus()
        self.page.locator('#picker button', has_text='ŋ').first.click()
        self.assertEqual(entry.input_value(), 'kuŋ')
        # inserts at the cursor, not just at the end
        entry.evaluate('e => e.setSelectionRange(1, 1)')
        self.page.locator('#picker button', has_text='ə').first.click()
        self.assertEqual(entry.input_value(), 'kəuŋ')
        entry.fill('kuŋ')
        self.page.click('button[name=submit]')
        self.page.wait_for_load_state('networkidle')
        self.lex1.refresh_from_db()
        self.assertEqual(self.lex1.entry, 'kuŋ')
        self.assertNoJSErrors()


class TestWordEdit(BrowserTestCase):
    def test_formset_edit_saves(self):
        self.login()
        self.open(reverse('word-edit', kwargs={'slug': 'hand'}))
        self.assertEqual(self.page.locator('#entryform tbody tr').count(), 2)
        self.page.fill(f'input[name$="-entry"][value="{self.lex1.entry}"]', 'kuu')
        self.page.click('button[name=submit]')
        self.page.wait_for_load_state('networkidle')
        self.lex1.refresh_from_db()
        self.assertEqual(self.lex1.entry, 'kuu')
        self.assertNoJSErrors()


class TestCognacy(BrowserTestCase):
    def test_assign_cognate_set(self):
        cogset = CognateSet.objects.create(protoform='*ku', editor=self.editor)
        self.login()
        self.open(reverse('cognacy:do', kwargs={'word': 'hand', 'clade': ''}))
        self.page.fill(f'#c-{self.lex1.pk}', str(cogset.pk))
        self.page.click('button:has-text("Save Changes")')
        self.page.wait_for_load_state('networkidle')
        self.assertTrue(Cognate.objects.filter(lexicon=self.lex1, cognateset=cogset).exists())
        self.assertNoJSErrors()


class TestCognacyIndex(BrowserTestCase):
    def test_pick_word_with_select2(self):
        self.login()
        self.open(reverse('cognacy:do_index'))
        self.select2('#id_word', 'hand')
        self.page.click('button[name=submit]')
        self.page.wait_for_load_state('networkidle')
        self.assertIn('/cognacy/do/hand', self.page.url)
        self.assertNoJSErrors()


class TestDataEntry(BrowserTestCase):

    def test_quick_entry_creates_task_and_saves_lexicon(self):
        self.login()
        self.open(reverse('entry:index'))
        # "Add New Language" opens the admin add form as a popup
        with self.page.expect_popup() as popup:
            self.page.click('#add_id_language')
        self.assertIn('_popup=1', popup.value.url)
        popup.value.close()

        self.select2('#id_language', 'kuman')
        self.select2('#id_source', 'trefry')
        self.page.fill('#id_records', '1')
        self.page.click('form[action$="quick"] button[name=submit]')
        self.page.wait_for_load_state('networkidle')
        task = Task.objects.get()
        self.assertIn(f'/entry/task/{task.pk}', self.page.url)
        rows = self.page.locator('#entryform tbody tr')
        self.assertEqual(rows.count(), 1)

        # the formset plugin adds and removes rows
        self.page.click('a:has-text("Add entry")')
        self.assertEqual(rows.count(), 2)
        added = rows.nth(1).locator('input[name$="-entry"]')
        added.focus()
        self.page.locator('#picker button', has_text='ʔ').first.click()
        self.assertEqual(added.input_value(), 'ʔ')
        rows.nth(1).locator('a.delete-row').click()
        self.assertEqual(rows.count(), 1)

        # every row must be filled (empty generated rows fail validation by design)
        self.select2('#id_form-0-word', 'hand')
        self.page.fill('#id_form-0-entry', 'nuŋ')
        self.page.click('button[name=submit]')
        self.page.wait_for_load_state('networkidle')
        self.assertTrue(Lexicon.objects.filter(entry='nuŋ', word=self.word, language=self.lang, source=self.source).exists())
        task.refresh_from_db()
        self.assertTrue(task.done)
        self.assertNoJSErrors()


class TestEntryValidation(BrowserTestCase):
    def test_error_tooltip(self):
        task = Task.objects.create(name='T', description='', editor=self.editor, language=self.lang,
                                   source=self.source, view='GenericView', records=1)
        self.login()
        self.open(reverse('entry:detail', kwargs={'task_id': task.pk}))
        self.page.click('button[name=submit]')  # empty row -> field errors
        self.page.wait_for_load_state('networkidle')
        self.page.hover('td.error .tip >> nth=0')
        self.page.wait_for_selector('.tooltip')
        self.assertIn('required', self.page.inner_text('.tooltip').lower())
        self.assertNoJSErrors()


class TestEntryWithImage(BrowserTestCase):
    def test_image_toolbar_sticks_and_zoomer_loads(self):
        task = Task.objects.create(
            name='Scan', description='', editor=self.editor, language=self.lang, source=self.source,
            image='data/2013-01/test.png', view='GenericView', records=40,
        )
        # the live server doesn't serve media: answer image requests with a page-sized PNG
        self.context.route('**/media/**', lambda route: route.fulfill(body=png(2000, 1500), content_type='image/png'))
        self.login()
        self.open(reverse('entry:detail', kwargs={'task_id': task.pk}))
        self.page.wait_for_selector('.zoomer-zoom-in')
        width = lambda: self.page.locator('.zoomer-image').bounding_box()['width']
        before = width()
        # zoomer zooms while the button is held down
        self.page.hover('.zoomer-zoom-in')
        self.page.mouse.down()
        self.page.wait_for_timeout(500)
        self.page.mouse.up()
        self.page.wait_for_timeout(300)
        self.assertGreater(width(), before)
        self.page.mouse.wheel(0, 3000)
        self.page.wait_for_timeout(300)
        self.assertLess(abs(self.page.locator('#scroller').bounding_box()['y']), 2)
        self.assertNoJSErrors()


class TestPublicPages(BrowserTestCase):
    def test_language_map_labels_fullscreen_spiderfy(self):
        # a second language at the same location, with markup in its name
        Language.objects.create(language='Ku<b>x</b>', slug='kux', isocode='kue', editor=self.editor)
        Lexicon.objects.create(language=Language.objects.get(slug='kux'), source=self.source, word=self.word, entry='a', editor=self.editor)
        self.open(reverse('maps:language-map'))
        self.page.wait_for_selector('.leaflet-tooltip')
        labels = self.page.locator('.leaflet-tooltip').all_inner_texts()
        self.assertEqual(sorted(labels), ['Ku<b>x</b>', 'Kuman'])  # shown as text, not markup
        self.assertEqual(self.page.locator('.leaflet-tooltip b').count(), 0)
        self.assertEqual(self.page.locator('.leaflet-control-zoom-fullscreen').count(), 1)
        # overlapping markers fan out when clicked
        self.page.locator('.leaflet-marker-icon').first.click(force=True)
        self.page.wait_for_selector('path.leaflet-interactive')
        self.assertNoJSErrors()

    def test_crowded_map_labels_on_hover_then_zoom(self):
        for i in range(60):
            iso = 'x%02d' % i
            lang = Language.objects.create(language=f'Lang{i}', slug=f'lang{i}', isocode=iso, editor=self.editor)
            Location.objects.create(isocode=iso, latitude=-6 + i / 10, longitude=145 + i / 10, editor=self.editor)
            Lexicon.objects.create(language=lang, source=self.source, word=self.word, entry='e', editor=self.editor)
        self.open(reverse('maps:language-map'))
        self.page.wait_for_selector('.leaflet-marker-icon')
        self.assertEqual(self.page.locator('.leaflet-tooltip').count(), 0)
        self.page.locator('.leaflet-marker-icon').nth(5).hover(force=True)
        self.page.wait_for_selector('.leaflet-tooltip')
        self.page.mouse.move(5, 5)
        # zoom in: labels become permanent
        for _ in range(3):
            self.page.click('.leaflet-control-zoom-in')
            self.page.wait_for_timeout(400)
        self.assertGreater(self.page.locator('.leaflet-tooltip').count(), 5)
        self.assertNoJSErrors()

    def test_word_map_labels(self):
        self.open(reverse('maps:word-map', kwargs={'slug': 'hand'}))
        self.page.wait_for_selector('.leaflet-tooltip')
        self.assertTrue(set(self.page.locator('.leaflet-tooltip').all_inner_texts()) <= {'ku', 'kan'})  # labels are entries
        self.assertNoJSErrors()

    def test_language_page_minimap(self):
        self.open(reverse('language-detail', kwargs={'language': 'kuman'}))
        self.page.wait_for_selector('#map .leaflet-marker-icon')
        self.assertNoJSErrors()

    def test_mobile_menu(self):
        self.page.set_viewport_size({'width': 390, 'height': 800})
        self.open('/')
        self.assertFalse(self.page.is_visible('#topnav a:has-text("Languages")'))
        self.page.click('.navbar-toggler')
        self.page.click('#topnav a:has-text("Languages")')
        self.page.wait_for_load_state('networkidle')
        self.assertTrue(self.page.url.endswith(reverse('language-index')))
        self.assertNoJSErrors()

    def test_statistics_charts_render(self):
        self.open(reverse('statistics:statistics'))
        self.assertGreater(self.page.evaluate('Object.keys(Chart.instances).length'), 0)
        self.assertNoJSErrors()

    def test_copy_citation_buttons(self):
        self.open('/')
        self.assertFalse(self.page.is_visible('#bibtex'))
        self.page.click('[data-copy=bibtex]')
        self.assertTrue(self.page.evaluate('navigator.clipboard.readText()').startswith('@article{greenhill2015,'))
        self.page.click('[data-copy=citation]')
        self.assertTrue(self.page.evaluate('navigator.clipboard.readText()').startswith('Greenhill SJ. 2015.'))
        self.assertNoJSErrors()
