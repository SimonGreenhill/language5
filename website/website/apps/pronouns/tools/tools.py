from django.db.models import Count
from website.apps.pronouns.models import PronounType, Pronoun
from website.apps.pronouns.models import ALIGNMENT_CHOICES, PERSON_CHOICES
from website.apps.pronouns.models import NUMBER_CHOICES, GENDER_CHOICES

def full_repr_row(p):
    """Build a string representation of the given pronoun `p`"""

    def _get(key, choices):
        if isinstance(key, basestring):
            for x, y in choices:
                if key == x:
                    return y
        else:
            return key[1]

    # handle objects
    if isinstance(p, Pronoun):
        if p.pronountype.gender is None:
            return " ".join([
                p.pronountype.get_person_display(),
                p.pronountype.get_number_display()
            ])
        else:
            return " ".join([
                p.pronountype.get_person_display(),
                p.pronountype.get_number_display(),
                p.pronountype.get_gender_display()
            ])
    elif isinstance(p, PronounType):
        if p.gender is None:
            return " ".join([
                p.get_person_display(),
                p.get_number_display()
            ])
        else:
            return " ".join([
                p.get_person_display(),
                p.get_number_display(),
                p.get_gender_display()
            ])
    # handle dictionary
    else:
        person = _get(p['person'], PERSON_CHOICES)
        number = _get(p['number'], NUMBER_CHOICES)

        if p['gender'] is None:
            return " ".join([person, number])
        else:
            gender = _get(p['gender'], GENDER_CHOICES)
            return " ".join([person, number, gender])


def short_repr_row(p):
    """Builds a short string representation of the given pronoun `p`"""
    if isinstance(p, Pronoun):
        newp = {
            'person': p.pronountype.person,
            'number': p.pronountype.number,
            'alignment': p.pronountype.alignment,
            'gender': p.pronountype.gender,
        }
    elif isinstance(p, PronounType):
        newp = {
            'person': p.person,
            'number': p.number,
            'alignment': p.alignment,
            'gender': p.gender,
        }
    else:
        newp = {
            'person': p['person'][0],
            'number': p['number'][0],
            'alignment': p['alignment'][0],
        }
        if p['gender'] is not None:
            newp['gender'] = p['gender'][0]
        else:
            newp['gender'] = None

    if newp['gender'] is None:
        return "%(person)s%(number)s %(alignment)s" % newp
    else:
        return "%(person)s%(number)s %(gender)s %(alignment)s" % newp

def add_pronoun_table(pronoun_set, filter_empty_rows=True):
    """Construct a table for the given pronoun set

    `filter_empty_rows` - leave out the rows that are empty.
    """
    # loop over the pronouns we've been given and fill a table of the cells.
    cells = {}
    for p in pronoun_set:
        label = full_repr_row(p)
        # get row or set it to (A, None), (S, None), (O, None), (P, None)
        # i.e. empty placeholders for each different ALIGNMENT
        cells[label] = cells.get(label,
            dict(zip(
                [_[0] for _ in ALIGNMENT_CHOICES],
                [None for _ in ALIGNMENT_CHOICES]
            ))
        )
        # Save the pronoun into the right row/alignment cell.
        cells[label][p.pronountype.alignment] = p
    # Now do the sorting of the table *rows*
    pronoun_rows = []
    # Sort
    ptype_rows = PronounType._generate_all_rows()
    for row in ptype_rows:
        wanted_label = full_repr_row(row)
        found_row = False
        # go through each label in the cells e.g. (1st person singular...etc)
        for label in cells:
            if wanted_label == label:
                found_row = True
                # Ignore empty rows?
                # only add this row if at LEAST one cell has something in it.
                if filter_empty_rows:
                    non_zero = 0
                    for cell, value in cells[label].items():
                        if value is not None and len(value.entries.all()) > 0:
                            non_zero += 1
                    if non_zero:  # at least one cell is not empty
                        pronoun_rows.append((label, cells[label]))
                else:
                    pronoun_rows.append((label, cells[label]))
        
        if not found_row:
            raise ValueError(
                "Unable to find expected row for Paradigm: %s"
                "- probably need to run _prefill_pronouns()" % wanted_label
            )
    if not filter_empty_rows:
        assert len(pronoun_rows) == len(ptype_rows)
    return pronoun_rows
