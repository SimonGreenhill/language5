from django.test import TestCase
from django.test.client import Client
from django.forms import ValidationError
from django.core.urlresolvers import reverse

from website.apps.cognacy.tests.data import DataMixin
from website.apps.lexicon.models import CognateSet, Cognate


class Test_Merge(DataMixin):
    """Tests the Cognate Save View"""
    url = reverse('cognacy:merge', kwargs={'word': 'hand', 'clade': ''})
    
    def setUp(self):
        super(Test_Merge, self).setUp()
        self.AuthenticatedClient = Client()
        self.AuthenticatedClient.login(username="admin", password="test")
        
        # Setup = 
        #   cogset_A (lex_a)
        #   cogset_B (lex_b)
        #   cogset_AB (lex_a, lex_b)
        self.cogset_A = CognateSet.objects.create(protoform='test-1', editor=self.editor)
        self.cogset_B = CognateSet.objects.create(protoform='test-2', editor=self.editor)
        self.cogset_AB = CognateSet.objects.create(protoform='test-3', editor=self.editor)
        # cogset 1
        Cognate.objects.create(lexicon=self.lex_a, cognateset=self.cogset_A, editor=self.editor)
        # cogset 2
        Cognate.objects.create(lexicon=self.lex_b, cognateset=self.cogset_B, editor=self.editor)
        # cogset 3
        Cognate.objects.create(lexicon=self.lex_a, cognateset=self.cogset_AB, editor=self.editor)
        Cognate.objects.create(lexicon=self.lex_b, cognateset=self.cogset_AB, editor=self.editor)
            
    def test_error_when_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             "/accounts/login/?next=%s" % self.url,
                             status_code=302, target_status_code=200)
        
    def test_get_fails(self):
        response = self.AuthenticatedClient.get(self.url)
        # should just bounce back to when not POSTed
        self.assertRedirects(response, 
            reverse('cognacy:do', kwargs={'word': 'hand', 'clade': ''}),
            status_code=302, target_status_code=200
        )
    
    def test_merge_moves_cognates(self):
        form_data = {
            'merge-old': self.cogset_A.id, 
            'merge-new': self.cogset_B.id, 
        }
        response = self.AuthenticatedClient.post(self.url, form_data)
        # should now have nothing in cogset_A = [],
        assert self.cogset_A.lexicon.count() == 0
        # should now have cogset_B = [a,b]
        assert self.lex_a in self.cogset_B.lexicon.all()
        assert self.lex_b in self.cogset_B.lexicon.all()
        # should now have an (UNCHANGED) cogset_AB =  [a,b] 
        assert self.lex_a in self.cogset_AB.lexicon.all()
        assert self.lex_b in self.cogset_AB.lexicon.all()
        
    def test_merge_moves_multiple_cognates(self):
        form_data = {
            'merge-old': self.cogset_AB.id, 
            'merge-new': self.cogset_A.id, 
        }
        response = self.AuthenticatedClient.post(self.url, form_data)
        # should now have a and b in cogset_A = [],
        assert self.cogset_A.lexicon.count() == 2
        assert self.lex_a in self.cogset_A.lexicon.all()
        assert self.lex_b in self.cogset_B.lexicon.all()
        
        # should now have cogset_B = [b] -- UNCHANGED
        assert self.lex_a not in self.cogset_B.lexicon.all()
        assert self.lex_b in self.cogset_B.lexicon.all()
        # should now have an empty cogset_AB =  []
        assert self.cogset_AB.lexicon.count() == 0
        
    def test_merge_removes_cognateset(self):
        form_data = {
            'merge-old': self.cogset_A.id, 
            'merge-new': self.cogset_B.id, 
        }
        response = self.AuthenticatedClient.post(self.url, form_data)
        # cogset 1 should be dead.
        with self.assertRaises(CognateSet.DoesNotExist):
            CognateSet.objects.get(pk=self.cogset_A.pk)
        
    def test_merge_doesnt_duplicate_cognates(self):
        form_data = {
            'merge-old': self.cogset_AB.id, 
            'merge-new': self.cogset_A.id, 
        }
        response = self.AuthenticatedClient.post(self.url, form_data)
        # should now have a and b in cogset_A = [],
        assert self.cogset_A.lexicon.count() == 2, "Duplicate still present!"
        assert self.lex_a in self.cogset_A.lexicon.all()
        assert self.lex_b in self.cogset_B.lexicon.all()

    def test_error_on_identical_cognate_sets(self):
        form_data = {
            'merge-old': self.cogset_A.id, 
            'merge-new': self.cogset_A.id, 
        }
        response = self.AuthenticatedClient.post(self.url, form_data)
        assert self.cogset_A.lexicon.count() == 1
        assert self.cogset_B.lexicon.count() == 1
        assert self.cogset_AB.lexicon.count() == 2
        # Expected no changes!
