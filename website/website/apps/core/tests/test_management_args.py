from django.core.management import get_commands, load_command_class
from django.test import SimpleTestCase


class TestPositionalArgs(SimpleTestCase):
    """Commands declaring `args` must accept positional arguments."""

    def test_positional_args_accepted(self):
        for name, app in get_commands().items():
            if not app.startswith('website.'):
                continue
            with self.subTest(command=name):
                try:
                    cmd = load_command_class(app, name)
                except ImportError as e:  # e.g. check_synonyms needs website/data/
                    self.skipTest(f'{name}: {e}')
                if not getattr(cmd, 'args', '') or name == 'import':  # import declares its own positional
                    continue
                options = cmd.create_parser('manage.py', name).parse_args(['a', 'b'])
                self.assertEqual(options.args, ['a', 'b'])
