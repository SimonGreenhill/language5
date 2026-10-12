from django.contrib.auth.models import User
from django.db.models import ProtectedError
from django.test import TestCase

from website.apps.core.models import Language, Source
from website.apps.lexicon.models import Word, Lexicon
from website.apps.entry.models import Task, TaskLog


class TestUserDeleteProtected(TestCase):
    """Deleting a user must not cascade into the data they edited."""

    @classmethod
    def setUpTestData(cls):
        cls.editor = User.objects.create_user('ed', 'ed@example.com', 'test')
        lang = Language.objects.create(language='A', slug='a', editor=cls.editor)
        source = Source.objects.create(year='1', author='X', slug='x', editor=cls.editor)
        word = Word.objects.create(word='Hand', slug='hand', editor=cls.editor)
        Lexicon.objects.create(language=lang, source=source, word=word, entry='e', editor=cls.editor)

    def test_editor_protected(self):
        with self.assertRaises(ProtectedError):
            self.editor.delete()
        self.assertEqual(Lexicon.objects.count(), 1)

    def test_tasklog_person_protected(self):
        other = User.objects.create_user('logger', 'l@example.com', 'test')
        task = Task.objects.create(name='t', description='', editor=self.editor, view='GenericView', records=1)
        TaskLog.objects.create(person=other, task=task, message='m')
        with self.assertRaises(ProtectedError):
            other.delete()

    def test_user_without_data_deletable(self):
        User.objects.create_user('empty', 'e@example.com', 'test').delete()
