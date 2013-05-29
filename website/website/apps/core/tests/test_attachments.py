from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

from website.apps.core.models import Language, Source, Attachment

class Test_Attachment(TestCase):
    """Tests the Attachments page"""
    fixtures = ['test_core.json']
    
    def setUp(self):
        self.client = Client()
        self.editor = User.objects.get(pk=1)
        self.language = Language.objects.get(pk=1)
        self.source = Source.objects.create(year=1991, author='Smith', 
                                    slug='smith1991', reference='S2',
                                    comment='c1', editor=self.editor)
        
        
    def test_no_attachments_on_language_details(self):
        response = self.client.get(self.language.get_absolute_url())
        assert len(Attachment.objects.all()) == 0
        self.assertEqual(response.status_code, 200)
        assert 'Files:' not in response.content
        
    def test_show_attachments_on_language_details(self):
        # create attachment
        a = Attachment.objects.create(
            editor = self.editor,
            language = self.language,
            source = self.source,
            file = 'simon.jpg'
        )
        response = self.client.get(self.language.get_absolute_url())
        
        assert len(Attachment.objects.all()) == 1
        assert len(self.language.attachment_set.all()) == 1
        self.assertEqual(response.status_code, 200)
        
        assert 'Files:' in response.content
        assert 'simon.jpg' in response.content


    def test_no_attachments_on_source_details(self):
        response = self.client.get(self.source.get_absolute_url())
        assert len(Attachment.objects.all()) == 0
        self.assertEqual(response.status_code, 200)
        assert 'Files:' not in response.content

    def test_show_attachments_on_source_details(self):
        # create attachment
        a = Attachment.objects.create(
            editor = self.editor,
            language = self.language,
            source = self.source,
            file = 'simon.jpg'
        )
        response = self.client.get(self.source.get_absolute_url())

        assert len(Attachment.objects.all()) == 1
        assert len(self.language.attachment_set.all()) == 1
        self.assertEqual(response.status_code, 200)

        assert 'Files:' in response.content
        assert 'simon.jpg' in response.content
