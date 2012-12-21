from django import forms

from website.apps.lexicon.models import Lexicon

class SimpleForm(forms.ModelForm):
    description = u'Single Lexical Entry'
    
    class Meta:
        model = Lexicon
    
