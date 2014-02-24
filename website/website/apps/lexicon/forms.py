# forms.py
from django import forms
from website.apps.lexicon.models import Lexicon

class LexiconForm(forms.ModelForm):
    class Meta:
        model = Lexicon
        exclude = ('added', 'editor', )
        

class WordForm(forms.ModelForm):
    class Meta:
        model = Lexicon
        fields = ['language', 'source', 'word', 'entry', 'annotation']
        widgets = {
            # set input size
            'annotation': forms.widgets.TextInput(attrs={'class': 'input-medium'}),
            'entry': forms.widgets.TextInput(attrs={'class': 'input-medium'}),
            'language': forms.widgets.Select(attrs={'class': 'input-medium'}),
            'source': forms.widgets.Select(attrs={'class': 'input-medium'}),
            'word': forms.widgets.Select(attrs={'class': 'input-medium'}),
        }
