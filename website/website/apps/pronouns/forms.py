from django import forms
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory, inlineformset_factory

from website.apps.core.models import Language, Family, Source
from website.apps.pronouns.models import Paradigm, Pronoun, Relationship

class ParadigmForm(forms.ModelForm):
    class Meta:
        model = Paradigm
        exclude = ('editor', 'added')


class SimplePronounForm(forms.ModelForm):
    class Meta:
        model = Pronoun
        fields = ('form', 'comment',)
        exclude = ('editor', 'added',)
        hidden = ('paradigm', 'alignment', 'person', 'number',)
        widgets = {
            'comment': forms.widgets.TextInput(attrs={'class': 'input-medium hide', 'placeholder': 'comment'}),
            'form': forms.widgets.TextInput(attrs={'class': 'input-medium',}),
        }

PronounFormSet = inlineformset_factory(Paradigm, Pronoun,
        can_delete=False, extra=0, form=SimplePronounForm)


class FullPronounForm(forms.ModelForm):
    class Meta:
        model = Pronoun
        fields = ('person', 'number', 'alignment', 'form', 'comment')
        exclude = ('editor', 'added', 'gender', 'paradigm')
        widgets = {
            'comment': forms.widgets.TextInput(attrs={'class': 'input-small', 'placeholder': 'comment'}),
            'form': forms.widgets.TextInput(attrs={'class': 'input-small', 'placeholder': 'form'}),
        }


class RelationshipForm(forms.ModelForm):
    def __init__(self, *args,**kwargs):
        super(RelationshipForm, self).__init__(*args, **kwargs)
        # print self.instance
        # print type(self.instance)
        # self.fields['pronoun1'].queryset = Pronoun.objects.filter(paradigm=self.instance)
        #self.fields['client'].queryset = Client.objects.filter(company=company)
    
    class Meta:
        model = Relationship
        exclude = ('editor', 'added', 'paradigm')
        hidden = ('id', 'paradigm')
        widgets = {
            'comment': forms.widgets.TextInput(attrs={'class': 'input-medium'}),
        }


RelationshipFormSet = inlineformset_factory(Paradigm, Relationship,
                            can_delete=True, extra=1, form=RelationshipForm)
