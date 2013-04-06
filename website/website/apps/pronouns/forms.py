from django import forms
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory

from website.apps.core.models import Language, Family, Source
from website.apps.pronouns.models import Paradigm, Pronoun, Relationship

class ParadigmForm(forms.ModelForm):
    class Meta:
        model = Paradigm
        exclude = ('editor', 'added')
    

class RelationshipForm(forms.ModelForm):
    
    # def __init__(self, *args, **kwargs):
    #     paradigm = kwargs.pop('paradigm', None)
    #     super(RelationshipForm, self).__init__(*args, **kwargs)
    #     if paradigm is not None:
    #         q = Pronoun.objects.filter(paradigm=paradigm)
    #         self.fields["pronoun1"].queryset = q
    #         self.fields["pronoun2"].queryset = q

    class Meta:
        model = Relationship
        exclude = ('editor', 'added', 'paradigm')
        widgets = {
            'comment': forms.widgets.TextInput(attrs={'class': 'input-medium'}),
        }


class SimplePronounForm(forms.ModelForm):
    class Meta:
        model = Pronoun
        fields = ('person', 'number', 'alignment', 'form', 'comment')
        exclude = ('editor', 'added', 'gender', 'paradigm')
        widgets = {
            'comment': forms.widgets.TextInput(attrs={'class': 'input-small', 'placeholder': 'comment'}),
            'form': forms.widgets.TextInput(attrs={'class': 'input-small', 'placeholder': 'form'}),
        }


class AdvancedPronounForm(forms.ModelForm):
    paradigm = forms.CharField(widget=forms.HiddenInput())
    alignment = forms.CharField(widget=forms.HiddenInput())
    person = forms.CharField(widget=forms.HiddenInput())
    number = forms.CharField(widget=forms.HiddenInput())
    
    class Meta:
        model = Pronoun
        fields = ('form', 'comment')
        exclude = ('editor', 'added', 'paradigm', 'alignment', 'person', 'number')
        widgets = {
            'comment': forms.widgets.TextInput(attrs={'class': 'input-small', 'placeholder': 'comment'}),
            'form': forms.widgets.TextInput(attrs={'class': 'input-small', 'placeholder': 'form'}),
        }
        

SimplePronounFormSet = modelformset_factory(Pronoun, form=SimplePronounForm)
RelationshipFormSet = modelformset_factory(Relationship, form=RelationshipForm)
# from django.utils.functional import curry
# RelationshipFormSet.form = staticmethod(curry(RelationshipFormSet, paradigm=paradigm))

AdvancedPronounFormSet = formset_factory(AdvancedPronounForm, extra=0)






