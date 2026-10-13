from django.test import SimpleTestCase


class TestSettings(SimpleTestCase):
    def test_no_secret_key_in_base(self):
        """SECRET_KEY must come from local.py, never the committed base settings."""
        from website.settings import base
        self.assertFalse(hasattr(base, 'SECRET_KEY'))

    def test_hsts_and_proxy_ssl_in_template(self):
        with open(__import__('website.settings', fromlist=['x']).__path__[0] + '/local.template') as f:
            template = f.read()
        for name in ('SECURE_PROXY_SSL_HEADER', 'SECURE_HSTS_SECONDS', 'SECRET_KEY'):
            self.assertIn(name, template)


class TestMapTilePolicy(SimpleTestCase):
    """OSM tile usage policy: send a Referer, use the https tile URL, attribute OSM."""

    def test_referrer_sent_cross_origin(self):
        from django.conf import settings
        self.assertEqual(settings.SECURE_REFERRER_POLICY, 'strict-origin-when-cross-origin')

    def test_tile_url(self):
        from django.template.loader import get_template
        for name in ('includes/map.html', 'maps/map.html'):
            source = open(get_template(name).origin.name).read()
            with self.subTest(template=name):
                self.assertIn("https://tile.openstreetmap.org/{z}/{x}/{y}.png", source)
                self.assertIn("openstreetmap.org/copyright", source)


class TestLogging(SimpleTestCase):
    """django.log must rotate and not record DEBUG noise (it reached 1.1 GB)."""

    def test_file_handlers_rotate(self):
        from django.conf import settings
        for name, handler in settings.LOGGING['handlers'].items():
            if handler['class'].endswith('RotatingFileHandler'):
                with self.subTest(handler=name):
                    self.assertGreater(handler['backupCount'], 0)

    def test_django_logger_not_debug(self):
        from django.conf import settings
        self.assertNotEqual(settings.LOGGING['loggers']['django']['level'], 'DEBUG')


class TestTemplateDefaults(SimpleTestCase):
    def test_local_template_does_not_disable_cache(self):
        import website.settings
        with open(website.settings.__path__[0] + '/local.template') as f:
            self.assertNotIn('DummyCache', f.read())

    def test_no_placeholder_admin_email(self):
        from django.conf import settings
        self.assertNotIn('test@example.com', [a[1] for a in settings.ADMINS])


class TestCollectstaticManifest(SimpleTestCase):
    """Production uses ManifestStaticFilesStorage; every referenced file must exist."""

    def test_collectstatic_with_manifest(self):
        import tempfile
        from django.core.management import call_command
        from django.test import override_settings
        with tempfile.TemporaryDirectory() as root, override_settings(
            STATIC_ROOT=root,
            STORAGES={'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
                      'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'}},
        ):
            call_command('collectstatic', interactive=False, verbosity=0)
