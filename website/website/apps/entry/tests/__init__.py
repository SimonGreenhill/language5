# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test.client import Client

from django.contrib.auth.models import User
from website.apps.core.models import Source, Language
from website.apps.lexicon.models import Word, Lexicon
from website.apps.entry.models import Task


class DataMixin(TestCase):
    
    def setUp(self, *args):
        self.client = Client()
        # some data
        self.file_testimage = "data/2013-01/test.png"
        self.editor = User.objects.create_user('admin',
                                               'admin@example.com', "test")
        self.source = Source.objects.create(
                year=1991,
                author='Smith',
                slug='Smith1991',
                reference='S2',
                comment='c1',
                editor=self.editor
        )
        self.task = Task.objects.create(
            editor=self.editor,
            name="Test Task",
            description="A Test of Data Entry",
            source=self.source,
            image=self.file_testimage,
            done=False,
            view="GenericView",
            records=1, # needed so we don't have too many empty forms to validate
        )
        
        self.lang = Language.objects.create(language='A', slug='langa', 
            information='i.1', classification='a, b',
            isocode='aaa', editor=self.editor)
            
        self.word = Word.objects.create(word='Hand', slug='hand', 
            full='a hand', editor=self.editor)
            
        # for formset validation
        self.form_data = {
            'form-TOTAL_FORMS': u'1',
            'form-INITIAL_FORMS': u'1',
            'form-MAX_NUM_FORMS': u'1000',
            'form-0-language': self.lang.id,
            'form-0-source': self.source.id,
            'form-0-word': self.word.id,
            'form-0-entry': 'simon',
            'form-0-annotation': 'comment',
            'submit': 'true',
        }