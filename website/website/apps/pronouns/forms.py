from django import forms
from django.forms.formsets import formset_factory
from django.template import RequestContext

from website.apps.core.models import Language, Family, Source
from website.apps.pronouns.models import Paradigm, Pronoun, Relationship

class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        exclude = ('editor', 'added', 'isocode', 'classification', 'information')
        widgets = {
            'information': forms.widgets.TextInput(attrs={'class': 'input-medium'}),
            'classification': forms.widgets.TextInput(attrs={'class': 'input-medium'}),
            'language': forms.widgets.TextInput(attrs={'class': 'input-medium'}),
            'family': forms.widgets.Select(attrs={'class': 'input-medium'}),
            'isocode': forms.widgets.TextInput(attrs={'class': 'input-medium'}),
        }


class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        exclude = ('editor', 'added', 'slug', 'bibtex')
        widgets = {
            'reference': forms.widgets.TextInput(attrs={'class': 'input-medium'}),
            'comment': forms.widgets.TextInput(attrs={'class': 'input-medium'}),
        }
        

class ParadigmForm(forms.ModelForm):
    class Meta:
        model = Paradigm
        exclude = ('editor', 'added', 'language', 'source')
        widgets = {
            'comment': forms.widgets.Textarea(attrs={'cols': 72, 'rows': 3}),
        }
    # make sure to set editor, added
    

class RelationshipForm(forms.ModelForm):
    
    class Meta:
        model = Relationship
        exclude = ('editor', 'added', 'paradigm')
        
        widgets = {
            'comment': forms.widgets.TextInput(attrs={'class': 'input-medium'}),
        }
        
        
RelationshipFormSet = formset_factory(RelationshipForm, extra=1)