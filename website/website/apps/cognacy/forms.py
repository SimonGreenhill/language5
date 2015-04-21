from django import forms
from website.apps.core.models import Language
from website.apps.lexicon.models import Word

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
