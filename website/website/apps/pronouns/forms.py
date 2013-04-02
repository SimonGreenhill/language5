from django import forms
from django.forms.formsets import formset_factory
from django.template import RequestContext

from website.apps.core.models import Language, Family, Source
from website.apps.pronouns.models import Paradigm, Pronoun, Relationship

class ParadigmForm(forms.ModelForm):
    class Meta:
        model = Paradigm
        exclude = ('editor', 'added')
        widgets = {
            'comment': forms.widgets.TextInput(attrs={'class': 'input-large'}),
        }
    

class RelationshipForm(forms.ModelForm):
    class Meta:
        model = Relationship
        exclude = ('editor', 'added', 'paradigm')
        
        widgets = {
            'comment': forms.widgets.TextInput(attrs={'class': 'input-medium'}),
        }
                
RelationshipFormSet = formset_factory(RelationshipForm, extra=1)



class SimplePronounForm(forms.ModelForm):
    class Meta:
        model = Pronoun
        fields = ('person', 'number', 'alignment', 'gloss', 'comment')
        exclude = ('editor', 'added', 'gender', 'paradigm')
        widgets = {
            'comment': forms.widgets.TextInput(attrs={'class': 'input-small', 'placeholder': 'comment'}),
            'gloss': forms.widgets.TextInput(attrs={'class': 'input-small', 'placeholder': 'gloss'}),
        }


class AdvancedPronounForm(forms.ModelForm):
    paradigm = forms.CharField(widget=forms.HiddenInput())
    alignment = forms.CharField(widget=forms.HiddenInput())
    person = forms.CharField(widget=forms.HiddenInput())
    number = forms.CharField(widget=forms.HiddenInput())
    
    class Meta:
        model = Pronoun
        fields = ('gloss', 'comment')
        exclude = ('editor', 'added', 'paradigm', 'alignment', 'person', 'number')
        widgets = {
            'comment': forms.widgets.TextInput(attrs={'class': 'input-small', 'placeholder': 'comment'}),
            'gloss': forms.widgets.TextInput(attrs={'class': 'input-small', 'placeholder': 'gloss'}),
        }
        
AdvancedPronounFormSet = formset_factory(AdvancedPronounForm, extra=0)






