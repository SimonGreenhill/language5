from website.apps.lexicon.models import CognateSet
from website.apps.cognacy.tests.data import DataMixin

from website.apps.cognacy.forms import MergeCognateForm, DoCognateForm, get_clades

class Test_GetClades(DataMixin):
    def test(self):
        #langa = 'a, a'
        #langb = 'a, b'
        clades = get_clades()
        assert ('', 'ALL (2)') in clades  # root
        assert (u'a', u'a (2)') in clades  # clade a, both languages
        assert (u'a, a', u'a, a (1)') in clades  # clade a, a - langa
        assert (u'a, b', u'a, b (1)') in clades  # clade a, b - langb


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
        
