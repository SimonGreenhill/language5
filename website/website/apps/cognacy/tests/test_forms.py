from website.apps.lexicon.models import CognateSet
from website.apps.cognacy.tests.data import DataMixin

from website.apps.cognacy.forms import MergeCognateForm

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
        
