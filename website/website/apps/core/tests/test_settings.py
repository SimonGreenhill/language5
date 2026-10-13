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
