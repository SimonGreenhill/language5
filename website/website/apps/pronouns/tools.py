from website.apps.pronouns.models import Pronoun
from website.apps.pronouns.forms import AdvancedPronounFormSet

def generate_pronoun_formsets(paradigm):
    formsets = []
    #stored = paradigm.pronoun_set.all()
    for p in Pronoun.PERSON_CHOICES:
        for n in Pronoun.NUMBER_CHOICES:
            key = "%s_%s" % (p[0], n[0])
            initial = []
            for a in Pronoun.ALIGNMENT_CHOICES:
                initial.append({
                    'person': p[0],
                    'number': n[0],
                    'alignment': a[0],
                })
            formsets.append(AdvancedPronounFormSet(initial=initial, prefix=key))
    return formsets
    
    