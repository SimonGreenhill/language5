from django import forms
from website.apps.core.models import Language
from website.apps.lexicon.models import Word, CognateSet

from collections import Counter

def get_clades(depth=3):
    clades = Counter()
    total = 0
    for o in Language.objects.values('classification'):
        if len(o['classification']) < 2:
            continue
        classif = [_.strip() for _ in o['classification'].split(',')]
        sub = []
        for i in range(0, min([depth, len(classif)])):
            sub.append(classif[i])
            clades[", ".join(sub)] += 1
        total += 1
        
    choices = sorted([(c, "%s (%d)" % (c, clades[c])) for c in clades])
    choices.insert(0, ('', 'ALL (%d)' % total))  # add default
    return choices
    

class DoCognateForm(forms.Form):
    word = forms.ModelChoiceField(
        queryset=Word.objects.order_by('word'),
        widget=forms.widgets.Select(attrs={'class': 'input-xxlarge'}),
        required=True
    )
    clade = forms.ChoiceField(
        choices=get_clades(),
        widget=forms.widgets.Select(attrs={'class': 'input-xxlarge'}),
        required=False
    )
    
    def __init__(self, *args, **kwargs):
        is_hidden = kwargs.pop('is_hidden', None)
        super(DoCognateForm, self).__init__(*args, **kwargs)
        if is_hidden:
            self.fields['word'].widget = forms.HiddenInput()
            self.fields['clade'].widget = forms.HiddenInput()



class MergeCognateForm(forms.Form):
    old = forms.ModelChoiceField(
        queryset=None,
    )
    new = forms.ModelChoiceField(
        queryset=None,
    )  
    
    def __init__(self, *args, **kwargs):
        queryset = kwargs.pop('queryset', None)
        super(MergeCognateForm, self).__init__(*args, **kwargs)
        self.fields['old'].queryset = queryset
        self.fields['new'].queryset = queryset
    
    def clean(self):
        cleaned_data = super(MergeCognateForm, self).clean()
        if cleaned_data.get('old', None) == cleaned_data.get('new', None):
            raise forms.ValidationError('The cognate sets cannot be the same!')
        return cleaned_data
        
    class Meta:
        model = CognateSet
        