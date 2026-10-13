from website.apps.lexicon.models import CognateSet
from website.apps.cognacy.tests.data import DataMixin

from website.apps.cognacy.forms import MergeCognateForm, DoCognateForm, get_clades

class Test_GetClades(DataMixin):
    def test(self):
        #langa = 'a, a'
        #langb = 'a, b'
        clades = get_clades()
        assert ('', 'ALL (2)') in clades  # root
        assert ('a', 'a (2)') in clades  # clade a, both languages
        assert ('a, a', 'a, a (1)') in clades  # clade a, a - langa
        assert ('a, b', 'a, b (1)') in clades  # clade a, b - langb


class Test_DoCognateForm(DataMixin):
    def test_empty_clades(self):
        form_data = {'word': self.word.id, 'clade': ''}
        d = DoCognateForm(form_data)
        assert d.fields['clade'].choices == []
    
    def test_clades(self):
        clades = [('', 'all'), ('clade1', 'subclade')]
        form_data = {'word': self.word.id, 'clade': 'clade1'}
        d = DoCognateForm(form_data, clades=clades)
        assert d.fields['clade'].choices == clades

    def test_validate_empty_clades(self):
        form_data = {'word': self.word.id, 'clade': ''}
        d = DoCognateForm(form_data)
        assert d.is_valid()
        
    def test_validate_clades(self):
        clades = [('', 'all'), ('clade1', 'subclade')]
        form_data = {'word': self.word.id, 'clade': 'clade1'}
        d = DoCognateForm(form_data, clades=clades)
        assert d.is_valid()
        

class Test_Forms(DataMixin):
    def test_ok(self):
        cogset_1 = CognateSet.objects.create(protoform='test-1', editor=self.editor)
        cogset_2 = CognateSet.objects.create(protoform='test-2', editor=self.editor)
        form_data = {
            'old': cogset_1.id, 
            'new': cogset_2.id, 
        }
        f = MergeCognateForm(form_data, queryset=CognateSet.objects.all())
        assert f.is_valid()
    
    def test_error_on_identical_cognate_sets(self):
        cogset_1 = CognateSet.objects.create(protoform='test-1', editor=self.editor)
        form_data = {
            'old': cogset_1.id, 
            'new': cogset_1.id, 
        }
        f = MergeCognateForm(form_data, queryset=CognateSet.objects.all())
        assert not f.is_valid()
        


from django.test import TestCase


class TestGetCladesNullClassification(TestCase):
    def test_null_classification_ignored(self):
        from django.contrib.auth.models import User
        from website.apps.core.models import Language
        from website.apps.cognacy.forms import get_clades
        from website.apps.core.templatetags.website_tags import condense_classification
        ed = User.objects.create_user('ed', 'e@example.com', 'test')
        Language.objects.create(language='A', slug='a', editor=ed, classification=None)
        Language.objects.create(language='B', slug='b', editor=ed, classification='TNG, Madang')
        self.assertEqual([c for c, _ in get_clades()], ['', 'TNG', 'TNG, Madang'])
        self.assertEqual(condense_classification(None), {'classif': []})
