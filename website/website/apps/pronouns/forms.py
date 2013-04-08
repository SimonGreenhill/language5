from django import forms
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory, inlineformset_factory

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


class FullPronounForm(forms.ModelForm):
    class Meta:
        model = Pronoun
        fields = ('person', 'number', 'alignment', 'form', 'comment')
        exclude = ('editor', 'added', 'gender', 'paradigm')
        widgets = {
            'comment': forms.widgets.TextInput(attrs={'class': 'input-small', 'placeholder': 'comment'}),
            'form': forms.widgets.TextInput(attrs={'class': 'input-small', 'placeholder': 'form'}),
        }


class SimplePronounForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SimplePronounForm, self).__init__(*args, **kwargs)
        #self.PARADIGM = repr()
    
    class Meta:
        model = Pronoun
        fields = ('form',)
        exclude = ('editor', 'added',)
        hidden = ('paradigm', 'alignment', 'person', 'number', 'comment',)
        widgets = {
            'comment': forms.widgets.TextInput(attrs={'class': 'input-small', 'placeholder': 'comment'}),
            'form': forms.widgets.TextInput(attrs={'class': 'input-medium',}),
        }
        
PronounFormSet = inlineformset_factory(Paradigm, Pronoun,
        can_delete=False, extra=0, form=SimplePronounForm)
        


# from django.forms.forms.models import BaseModeFormSet
# 
# PRONOUN_SEQUENCE = Pronoun._generate_all_combinations()
# 
# class TabledPronounFormSet(BaseModelFormSet):
#     model = Pronoun
#     def __init__(self, *args, **kwargs):
#         paradigm = kwargs.pop('paradigm')
#         super(TabledPronounFormSet, self).__init__(*args, **kwargs)
#         self.queryset = Pronoun.objects.filter(name__startswith='O')
# 
# f = TabledPronounFormSet(form=SimplePronounForm)
# #pfs = modelformset_factory(Pronoun, form=AdvancedPronounForm, formset=TabledPronounFormSet)
# 
# 
# 


# DELETE ME -----------------------------------------------#
class PronounParadigmForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        paradigm = kwargs.pop('paradigm')
        pronouns = paradigm.pronoun_set.all()
        super(PronounParadigmForm, self).__init__(*args, **kwargs)
        self.pronoun_fieldsets = {}
        self.pronoun_ids = []
        for comb in Pronoun._generate_all_combinations():
            pronoun_id = None
            pronoun_value = ""
            for p in pronouns:
                this_comb = (p.person, p.number, p.gender, p.alignment)
                if comb == this_comb:
                    pronoun_value = p.form
                    pronoun_id = p.id
            
            field_id = "%s_id" % "_".join(comb)
            field_name = "_".join(comb)
            self.fields[field_name] = forms.CharField(label=field_name, initial=pronoun_value, required=False)
            self.fields[field_id] = forms.IntegerField(widget=forms.HiddenInput(), initial=pronoun_id)

            # make fieldset
            row = " ".join(comb[0:3])
            self.pronoun_fieldsets[row] = self.pronoun_fieldsets.get(row, {})
            self.pronoun_fieldsets[row][comb[3]] = self.fields[field_name]
            self.pronoun_ids.append(self.fields[field_id])
    
    class Meta:
        model = Paradigm




#SimplePronounFormSet = modelformset_factory(Pronoun, form=SimplePronounForm)
#RelationshipFormSet = modelformset_factory(Relationship, form=RelationshipForm)
#AdvancedPronounFormSet = modelformset_factory(Pronoun, form=AdvancedPronounForm, extra=0)

# 