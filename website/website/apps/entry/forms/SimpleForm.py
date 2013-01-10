from django import forms

from website.apps.lexicon.models import Lexicon

class SimpleForm(forms.ModelForm):
    description = u'Single Lexical Entry'
    template = u"entry/includes/single_lexicon.html"
    
    class Meta:
        model = Lexicon
        exclude = ('editor', 'phon_entry', 'loan') 
        # over-ride Textarea for annotation
        widgets = {'annotation': forms.widgets.TextInput(),}
        #attrs={'max_length': 100}
    # make sure to set editor, added, and loan if loan_source is specified