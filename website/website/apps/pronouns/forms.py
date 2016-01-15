from django import forms
from django.forms.models import modelformset_factory, inlineformset_factory

from website.apps.lexicon.models import Lexicon
from website.apps.pronouns.models import Paradigm, PronounType, Relationship
from website.apps.pronouns.models import PERSON_CHOICES, NUMBER_CHOICES
from website.apps.pronouns.models import GENDER_CHOICES, ALIGNMENT_CHOICES

from website.apps.pronouns.tools import full_repr_row

INPUT_SMALL = {'class': 'input-small', }
INPUT_TINY = {'class': 'input-tiny', }

class CopyForm(forms.Form):
    pass


class ParadigmForm(forms.ModelForm):
    class Meta:
        model = Paradigm
        fields = ['language', 'label', 'source', 'analect', 'comment']
        widgets = {
            'comment': forms.widgets.Textarea(attrs={
                'cols': 60, 'rows': 5, 'class': 'field span12'}
            ),
        }

#-----------------------------------------------------------------
# ENTRIES

class LexiconForm(forms.ModelForm):
    entry = forms.CharField(required=False)
    
    class Meta:
        model = Lexicon
        hidden = ('id',)
        fields = ['entry', 'annotation']
        widgets = {
            'entry': forms.widgets.TextInput(attrs=INPUT_SMALL),
            'annotation': forms.widgets.TextInput(attrs={
                'class': 'input-small hide', 'placeholder': 'comment'
            }),
        }


# get all our formsets
# BRUTALLY SLOW
def create_pronoun_formset(paradigm, postdata=None):
    formsets = []
    pset = paradigm.pronoun_set.all().filter(pronountype__active=True)
    pset = pset.select_related('pronountype').prefetch_related('entries')
    for pronoun in pset:
        qset = pronoun.entries.all()
        extra = 0 if len(qset) else 1
        EntriesFormSet = modelformset_factory(
            Lexicon, form=LexiconForm, extra=extra
        )
        formset = EntriesFormSet(
            postdata,
            queryset=qset,
            prefix='%d_%d' % (pronoun.paradigm_id, pronoun.id)
        )
        formsets.append((pronoun, formset))
    return formsets
    
def sort_formset(formsets):
    """
    Sort formset for template view appropriately.
    
    Returns a list of dicts
    
    [
        (rowname, {A:.., S:...}),
        (rowname, {A:.., S:...}),
        (rowname, {A:.., S:...}),
    ]
    """
    ptypes = dict([
        (p['sequence'], p) for p in PronounType.objects.all().values()
    ])
    rows = {}
    
    empty = dict(zip(
        [x[0] for x in ALIGNMENT_CHOICES],
        [None for x in ALIGNMENT_CHOICES]
    ))
    
    # use decorate-sort-undecorate pattern to loop over pronoun and formset
    # in formsets. The sort key is the pronountype.sequence + 3 / 4
    # add three to get the grouping right (1-4), (5-8), (9-12) etc
    for pronoun, formset in formsets:
        pt = ptypes[pronoun.pronountype.sequence]
        row = full_repr_row(pt)
        sortkey = (pronoun.pronountype.sequence + 3) / 4
        rows[(sortkey, row)] = rows.get((sortkey, row), empty.copy())
        rows[(sortkey, row)][pt['alignment']] = formset
    
    return [(key, rows[(_, key)]) for (_, key) in sorted(rows)]


def save_pronoun_formset(paradigm, pronoun, formset, user):
    """
    >>> for pronoun, formset in create_pronoun_formset(paradigm, postdata):
    >>>     saved = save_pronoun_formset(paradigm, pronoun, formset, user)
    """
    pks = []
    if not formset.has_changed():
        # short circuit exit if no changes.
        return pks
    
    instances = formset.save(commit=False)
    for lex in instances:
        # keep things with entries
        if len(lex.entry.strip()) > 0:
            lex.editor = user                        # inject editor
            lex.word = pronoun.pronountype.word      # inject word
            lex.source = paradigm.source             # inject source
            lex.language = paradigm.language         # inject language
            lex.save()
            pks.append(lex.id)
            # and add to pronoun entries.
            pronoun.entries.add(lex)
            pronoun.save()
        # remove empty forms.
        else:
            lex.delete()
    return pks

def pronoun_formsets_are_valid(formsets):
    """Tests if all formsets are valid"""
    for pronoun, formset in formsets:
        if not formset.is_valid():
            return False
    return True


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
            'comment': forms.widgets.TextInput(attrs={
                'class': 'input-medium'
            }),
        }


RelationshipFormSet = inlineformset_factory(
    Paradigm, Relationship, can_delete=True, extra=1, form=RelationshipForm
)



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
            'alignment_one': forms.widgets.Select(INPUT_TINY),
            'person_one': forms.widgets.Select(INPUT_SMALL),
            'number_one': forms.widgets.Select(INPUT_SMALL),
            'gender_one': forms.widgets.Select(INPUT_SMALL),
            'alignment_two': forms.widgets.Select(INPUT_SMALL),
            'person_two': forms.widgets.Select(INPUT_SMALL),
            'number_two': forms.widgets.Select(INPUT_SMALL),
            'gender_two': forms.widgets.Select(INPUT_SMALL),
        }
