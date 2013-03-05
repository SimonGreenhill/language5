from django import forms
from django.forms.formsets import formset_factory

from website.apps.lexicon.models import Lexicon

class SimpleForm(forms.ModelForm):
    description = u'Single Lexical Entry'
    
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


class SimpleFormForLanguage(forms.ModelForm):
    description = u'Single Lexical Entry for a given language'

    class Meta:
        model = Lexicon
        exclude = ('editor', 'phon_entry', 'loan', 'loan_source', 'language') 
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

    
SimpleFormSet = formset_factory(SimpleForm, extra=40)


# class CognateForm(forms.ModelForm):
#     pass