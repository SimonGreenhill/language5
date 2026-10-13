import os

from django.conf import settings
from django.test import TestCase, override_settings
from django.test.client import Client

from django.contrib.auth.models import User
from website.apps.core.models import Source, Language
from website.apps.lexicon.models import Word
from website.apps.entry.models import Task


# the test image lives in the repo's media/, not the deployment's MEDIA_ROOT
REPO_MEDIA = os.path.join(os.path.dirname(settings.SITE_ROOT), 'media')


@override_settings(MEDIA_ROOT=REPO_MEDIA)
class DataMixin(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        # some data
        cls.file_testimage = "data/2013-01/test.png"
        cls.editor = User.objects.create_user(
            'admin', 'admin@example.com', "test"
        )
        cls.source = Source.objects.create(
            year="1991",
            author='Smith',
            slug='Smith1991',
            reference='S2',
            comment='c1',
            editor=cls.editor
        )
        cls.lang = Language.objects.create(
            language='A',
            slug='langa',
            information='i.1',
            classification='a, b',
            isocode='aaa',
            editor=cls.editor
        )
        cls.task = Task.objects.create(
            editor=cls.editor,
            name="Test Task",
            description="A Test of Data Entry",
            source=cls.source,
            image=cls.file_testimage,
            language=cls.lang,
            done=False,
            checkpoint=None,
            view="GenericView",
            records=1, # needed so we don't have too many empty forms to validate
        )
        cls.word = Word.objects.create(
            word='Hand',
            slug='hand',
            full='a hand',
            editor=cls.editor
        )
            
        # for formset validation
        cls.form_data = {
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '1',
            'form-MAX_NUM_FORMS': '1000',
            'form-0-language': cls.lang.id,
            'form-0-source': cls.source.id,
            'form-0-word': cls.word.id,
            'form-0-entry': 'simon',
            'form-0-annotation': 'comment',
            'submit': 'true',
        }