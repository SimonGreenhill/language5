from django import forms
from django.forms.formsets import formset_factory
from django.forms.models import BaseModelFormSet, inlineformset_factory

from website.apps.lexicon.models import Lexicon
from website.apps.pronouns.models import Paradigm, Pronoun, Relationship
from website.apps.pronouns.models import PERSON_CHOICES, NUMBER_CHOICES
from website.apps.pronouns.models import GENDER_CHOICES, ALIGNMENT_CHOICES

class ParadigmForm(forms.ModelForm):
    class Meta:
        model = Paradigm
        exclude = ('editor', 'added')

#-----------------------------------------------------------------
# ENTRIES

class SimplePronounLexiconForm(forms.ModelForm):
    # replace model select with charfields
    entries = forms.CharField()
    comment = forms.CharField(required=False) 
    
    def __init__(self, *args, **kwargs):
        super(SimplePronounLexiconForm, self).__init__(*args, **kwargs)
        entries, comments = [], []
        for e in self.instance.entries.all():
            entries.append(e.entry)
            comments.append(e.annotation)
        self.fields['entries'].initial = ", ".join(entries)
        self.fields['comment'].initial = ", ".join(comments)
        #self.initial['entries'] = ", ".join(entries)
        #self.initial['comment'] = ", ".join(comments)
        
        
    class Meta:
        model = Pronoun
        fields = ('entries', 'comment', 'pronountype')
        exclude = ('editor', 'added', 'paradigm')
        widgets = {
            'entry': forms.widgets.TextInput(attrs={'class': 'input-medium',}),
            'annotation': forms.widgets.TextInput(attrs={'class': 'input-medium hide', 'placeholder': 'comment'}),
        }
        
PronounFormSet = inlineformset_factory(Paradigm, Pronoun,
         can_delete=False, extra=0, form=SimplePronounLexiconForm)

#>>> AuthorFormSet = modelformset_factory(Author, formset=BaseAuthorFormSet)



# PronounFormSet = inlineformset_factory(Paradigm, Pronoun,
#         can_delete=False, extra=0, form=SimpleLexiconForm)

#-----------------------------------------------------------------
# RELATIONSHIPS
class RelationshipForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
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



#-----------------------------------------------------------------
# RULES
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
