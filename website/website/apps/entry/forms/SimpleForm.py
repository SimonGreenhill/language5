from django import forms
from django.forms.formsets import formset_factory

from website.apps.lexicon.models import Lexicon

class SimpleForm(forms.ModelForm):
    description = u'Single Lexical Entry'
    
    class Meta:
        model = Lexicon
        exclude = ('editor', 'phon_entry', 'loan', 'loan_source') 
        # over-ride Textarea for annotation
        widgets = {'annotation': forms.widgets.TextInput(),}
        #attrs={'max_length': 100}
    # make sure to set editor, added, and loan if loan_source is specified
    
#SimpleFormSet = formset_factory(SimpleForm, extra=20)


# class CognateForm(forms.ModelForm):
#     pass