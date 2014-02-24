# forms.py
from django import forms
from website.apps.core.models import Language, Source
from website.apps.lexicon.models import Word, Lexicon

class LexiconForm(forms.ModelForm):
    class Meta:
        model = Lexicon
        exclude = ('added', 'editor', )
        

class WordForm(forms.ModelForm):
    language = forms.ModelChoiceField(queryset=Language.cache_all_method.all().order_by('slug'))
    word = forms.ModelChoiceField(queryset=Word.cache_all_method.all().order_by('word'))
    source = forms.ModelChoiceField(queryset=Source.cache_all_method.all().order_by('slug'))
    
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
