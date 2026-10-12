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
