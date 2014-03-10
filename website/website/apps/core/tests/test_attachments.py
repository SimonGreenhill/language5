from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

from website.apps.core.models import Language, Source, Attachment

class DataMixin(TestCase):

    fixtures = ['test_core.json']

    def setUp(self):
        self.client = Client()
        self.editor = User.objects.create_user('admin',
                                               'admin@example.com', "test")
        self.language = Language.objects.get(pk=1)
        self.source = Source.objects.create(year="1991", author='Smith', 
                                    slug='smith1991', reference='S2',
                                    comment='c1', editor=self.editor)
        self.att = Attachment.objects.create(
            editor = self.editor,
            language = self.language,
            source = self.source,
            file = 'simon.jpg'
        )
        

class Test_Attachment_LanguageDetails(DataMixin):
    """Tests the Attachments on the LanguageDetails page"""
    
    def test_no_attachments(self):
        response = self.client.get(Language.objects.get(pk=2).get_absolute_url())
        self.assertEqual(response.status_code, 200)
        assert 'Files:' not in response.content
        
    def test_show_attachments_to_logged_in(self):
        self.client.login(username="admin", password="test")
        response = self.client.get(self.language.get_absolute_url())
        assert len(self.language.attachment_set.all()) == 1
        self.assertEqual(response.status_code, 200)
        
        assert 'Files:' in response.content
        assert 'simon.jpg' in response.content

    def test_do_not_show_attachments_to_anonymous(self):
        response = self.client.get(self.language.get_absolute_url())
        assert len(self.language.attachment_set.all()) == 1
        self.assertEqual(response.status_code, 200)
        
        assert 'Files:' not in response.content
        assert 'simon.jpg' not in response.content


class Test_Attachment_SourceDetails(DataMixin):
    """Tests the Attachments on the SourceDetails page"""

    def test_no_attachments(self):
        response = self.client.get(self.source.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        assert 'Files:' not in response.content

    def test_show_attachments_to_logged_in(self):
        self.client.login(username="admin", password="test")
        response = self.client.get(self.source.get_absolute_url())
        assert len(self.language.attachment_set.all()) == 1
        self.assertEqual(response.status_code, 200)

        assert 'Files:' in response.content
        assert 'simon.jpg' in response.content

    def test_do_not_show_attachments_to_anonymous(self):
        response = self.client.get(self.source.get_absolute_url())
        assert len(self.language.attachment_set.all()) == 1
        self.assertEqual(response.status_code, 200)

        assert 'Files:' not in response.content
        assert 'simon.jpg' not in response.content
