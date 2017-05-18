from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

from website.apps.core.models import Language, Source, Attachment
from website.apps.core.tests.test_views import BaseMixin

class AttachmentDataMixin(BaseMixin):
    @classmethod
    def setUpTestData(cls):
        super(AttachmentDataMixin, cls).setUpTestData()
        cls.att = Attachment.objects.create(
            editor=cls.editor,
            language=cls.language1,
            source=cls.source1,
            file='simon.jpg'
        )
        

class Test_Attachment_LanguageDetails(AttachmentDataMixin, TestCase):
    """Tests the Attachments on the LanguageDetails page"""
    def test_no_attachments(self):
        response = self.client.get(self.language2.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        assert b'Files:' not in response.content
        
    def test_show_attachments_to_logged_in(self):
        self.client.login(username="admin", password="test")
        response = self.client.get(self.language1.get_absolute_url())
        assert len(self.language1.attachment_set.all()) == 1
        self.assertEqual(response.status_code, 200)
        
        assert b'Files:' in response.content
        assert b'simon.jpg' in response.content

    def test_do_not_show_attachments_to_anonymous(self):
        response = self.client.get(self.language1.get_absolute_url())
        assert len(self.language1.attachment_set.all()) == 1
        self.assertEqual(response.status_code, 200)
        
        assert b'Files:' not in response.content
        assert b'simon.jpg' not in response.content


class Test_Attachment_SourceDetails(AttachmentDataMixin, TestCase):
    """Tests the Attachments on the SourceDetails page"""

    def test_no_attachments(self):
        response = self.client.get(self.source2.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        assert b'Files:' not in response.content

    def test_show_attachments_to_logged_in(self):
        self.client.login(username="admin", password="test")
        response = self.client.get(self.source1.get_absolute_url())
        assert len(self.language1.attachment_set.all()) == 1
        self.assertEqual(response.status_code, 200)

        assert b'Files:' in response.content
        assert b'simon.jpg' in response.content

    def test_do_not_show_attachments_to_anonymous(self):
        response = self.client.get(self.source1.get_absolute_url())
        assert len(self.language1.attachment_set.all()) == 1
        self.assertEqual(response.status_code, 200)

        assert b'Files:' not in response.content
        assert b'simon.jpg' not in response.content
