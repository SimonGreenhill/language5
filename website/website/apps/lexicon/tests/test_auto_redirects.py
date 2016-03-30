from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.contrib.redirects.models import Redirect

from website.apps.core.tests.test_auto_redirects import RedirectionTestMixin
from website.apps.lexicon.models import Word, WordSubset
    
class TestRedirectionWord(RedirectionTestMixin, TestCase):
    def setUp(self):
        super(RedirectionTestMixin, self).setUp()
        self.word = Word.objects.create(
            word='Hand', slug='hand', full='a hand', editor=self.editor
        )
        self.subset = WordSubset.objects.create(
            subset='All words', 
            slug='all', description="Everthing", 
            editor=self.editor
        )
    model = Word

