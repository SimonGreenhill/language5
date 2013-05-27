from django import forms
from website.apps.core.models import Language, Source
from website.apps.lexicon.models import Lexicon, Word
from website.apps.entry.models import Wordlist


class QuickEntryViewForm(forms.Form):
    records = forms.IntegerField(
        initial=5,
        widget=forms.widgets.TextInput(attrs={'class': 'input-mini'})
    )
    language = forms.ModelChoiceField(
        queryset=Language.objects.order_by('slug'),
        widget=forms.widgets.Select(attrs={'class': 'input-medium'}),
        required=False
    )
    wordlist = forms.ModelChoiceField(
        queryset=Wordlist.objects.order_by('name'),
        widget=forms.widgets.Select(attrs={'class': 'input-medium'}),
        required=False
    )
    source = forms.ModelChoiceField(
        queryset=Source.objects.order_by('slug'),
        widget=forms.widgets.Select(attrs={'class': 'input-medium'})
    )
    
            
