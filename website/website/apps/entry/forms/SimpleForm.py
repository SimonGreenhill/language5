from django import forms
from django.forms.formsets import formset_factory

from website.apps.lexicon.models import Lexicon

class GenericForm(forms.ModelForm):
    class Meta:
        model = Lexicon
        exclude = ('editor', 'phon_entry', 'loan', 'loan_source') 
        widgets = {
            # over-ride Textarea for annotation
            'annotation': forms.widgets.TextInput(attrs={'class': 'input-small'}),
            
            # and set input-small
            'entry': forms.widgets.TextInput(attrs={'class': 'input-small'}),
            'language': forms.widgets.Select(attrs={'class': 'input-small'}),
            'source': forms.widgets.Select(attrs={'class': 'input-small'}),
            'word': forms.widgets.Select(attrs={'class': 'input-small'}),
        }
    # make sure to set editor, added, and loan if loan_source is specified

GenericFormSet = formset_factory(GenericForm, extra=40)
