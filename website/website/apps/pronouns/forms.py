from django import forms
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory, inlineformset_factory

from website.apps.core.models import Language, Family, Source
from website.apps.pronouns.models import Paradigm, Pronoun, Relationship
from website.apps.pronouns.models import PERSON_CHOICES, NUMBER_CHOICES
from website.apps.pronouns.models import GENDER_CHOICES, ALIGNMENT_CHOICES

class ParadigmForm(forms.ModelForm):
    class Meta:
        model = Paradigm
        exclude = ('editor', 'added')


class SimplePronounForm(forms.ModelForm):
    class Meta:
        model = Pronoun
        fields = ('entries', 'comment',)
        exclude = ('editor', 'added',)
        hidden = ('paradigm',)
        widgets = {
            'comment': forms.widgets.TextInput(attrs={'class': 'input-medium hide', 'placeholder': 'comment'}),
            'entries': forms.widgets.TextInput(attrs={'class': 'input-medium',}),
        }

PronounFormSet = inlineformset_factory(Paradigm, Pronoun,
        can_delete=False, extra=0, form=SimplePronounForm)


class RelationshipForm(forms.ModelForm):
    def __init__(self, *args,**kwargs):
        super(RelationshipForm, self).__init__(*args, **kwargs)
    
    class Meta:
        model = Relationship
        exclude = ('editor', 'added', 'paradigm')
        hidden = ('id', 'paradigm')
        widgets = {
            'comment': forms.widgets.TextInput(attrs={'class': 'input-medium'}),
        }


RelationshipFormSet = inlineformset_factory(Paradigm, Relationship,
                            can_delete=True, extra=1, form=RelationshipForm)


# Prepend --- to these choice fields for the RuleForm.
alignment_choices = [("---", "-")]
alignment_choices.extend(ALIGNMENT_CHOICES)
person_choices = [("---", "-")]
person_choices.extend(PERSON_CHOICES)
number_choices = [("---", "-")]
number_choices.extend(NUMBER_CHOICES)
gender_choices = [("---", "-")]
gender_choices.extend(GENDER_CHOICES)
relationship_choices = [("---", "-")]
relationship_choices.extend(Relationship.RELATIONSHIP_CHOICES)

class RuleForm(forms.Form):
    alignment_one = forms.ChoiceField(alignment_choices)
    person_one = forms.ChoiceField(person_choices)
    number_one = forms.ChoiceField(number_choices)
    gender_one = forms.ChoiceField(gender_choices)
    relationship = forms.ChoiceField(relationship_choices)
    alignment_two = forms.ChoiceField(alignment_choices)
    person_two = forms.ChoiceField(person_choices)
    number_two = forms.ChoiceField(number_choices)
    gender_two = forms.ChoiceField(gender_choices)
    
    class Meta:
        widgets = {
            'alignment_one': forms.widgets.Select(attrs={'class': 'input-tiny'}),
            'person_one': forms.widgets.Select(attrs={'class': 'input-small'}),
            'number_one': forms.widgets.Select(attrs={'class': 'input-small'}),
            'gender_one': forms.widgets.Select(attrs={'class': 'input-small'}),
            'alignment_two': forms.widgets.Select(attrs={'class': 'input-small'}),
            'person_two': forms.widgets.Select(attrs={'class': 'input-small'}),
            'number_two': forms.widgets.Select(attrs={'class': 'input-small'}),
            'gender_two': forms.widgets.Select(attrs={'class': 'input-small'}),
        }
