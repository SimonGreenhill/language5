# forms.py
from django import forms
from website.apps.lexicon.models import Lexicon

class LexiconForm(forms.ModelForm):
    class Meta:
        model = Lexicon
        exclude = ('added', 'editor', )