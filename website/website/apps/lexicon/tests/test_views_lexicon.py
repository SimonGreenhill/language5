from django.test import TestCase
from django.core.urlresolvers import reverse

from website.apps.lexicon.tests import DataMixin
from website.apps.lexicon.models import Lexicon


class Test_LexiconDetail(DataMixin, TestCase):
    def setUp(self):
        super(Test_LexiconDetail, self).setUp()
        self.url = reverse('lexicon-detail', kwargs={'pk': self.lexicon1.id})
        self.response = self.client.get(self.url)
    
    def test_200ok(self):
        self.assertEquals(self.response.status_code, 200)
    
    def test_template(self):
        self.assertTemplateUsed(self.response, 'lexicon/lexicon_detail.html')
    
    def test_get_missing(self):
        response = self.client.get(reverse('lexicon-detail', kwargs={'pk': 5}))
        self.assertEquals(response.status_code, 404)
    
    def test_get_data(self):
        self.assertEquals(self.response.status_code, 200)
        assert 'A' in self.response.content
        

class Test_LexiconEditNotLoggedIn(DataMixin, TestCase):
    def setUp(self):
        super(Test_LexiconEditNotLoggedIn, self).setUp()
        self.url = reverse('lexicon-edit', kwargs={'pk': self.lexicon1.id})
    
    def test_error_on_notlogged_in(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(
            response, "/accounts/login/?next=%s" % self.url,
            status_code=302, target_status_code=200
        )



class Test_LexiconEdit(DataMixin, TestCase):
    def setUp(self):
        super(Test_LexiconEdit, self).setUp()
        self.url = reverse('lexicon-edit', kwargs={'pk': self.lexicon1.id})
        self.client.login(username="admin", password="test")
        self.response = self.client.get(self.url)
        
        
    def get_post_data(self, obj):
        skip = ('added', 'editor_id', 'loan_source_id', 'loan')
        return dict([
            (k.replace("_id", ""), v) for k, v in obj.__dict__.items()
            if not k.startswith("_") and k not in skip
        ])
    
    def test_200ok_logged_in(self):
        self.assertEquals(self.response.status_code, 200)
    
    def test_template(self):
        self.assertTemplateUsed(self.response, 'lexicon/lexicon_edit.html')
    
    def test_error_on_missing(self):
        response = self.client.get(reverse('lexicon-edit', kwargs={'pk': 500000}))
        self.assertEquals(response.status_code, 404)
        
    def test_get(self):
        self.assertEquals(self.response.status_code, 200)
        assert 'A' in self.response.content
        
    def test_post(self):
        postdata = self.get_post_data(self.lexicon1)
        postdata['entry'] = 'banana'
        response = self.client.post(self.url, postdata, follow=True)
        self.assertEquals(response.status_code, 200)
        assert 'banana' in response.content
        
    def test_update_editor(self):
        from django.contrib.auth.models import User
        assert self.lexicon1.editor == self.editor
        newuser = User.objects.create_user('dave', 'dave@dave.com', 'secret')
        self.client.login(username="dave", password="secret")
        response = self.client.post(
            self.url, self.get_post_data(self.lexicon1), follow=True
        )
        self.assertEquals(response.status_code, 200)
        if Lexicon.objects.get(pk=self.lexicon1.id).editor != newuser:
            raise AssertionError("Have not updated editor!")
        
    def test_update_added(self):
        added = self.lexicon1.added
        self.client.login(username="admin", password="test")
        self.client.post(self.url, self.get_post_data(self.lexicon1), follow=True)
        now = Lexicon.objects.get(pk=self.lexicon1.id).added
        assert now > added, "%r is not larger than %r" % (now, added)
        
    def test_create_revision(self):
        from reversion.models import Version
        version_list = Version.objects.get_for_object(self.lexicon1)
        assert len(version_list) == 0
        self.client.login(username="admin", password="test")
        self.client.post(self.url, self.get_post_data(self.lexicon1), follow=True)
        version_list = Version.objects.get_for_object(self.lexicon1)
        assert len(version_list) == 1
    
