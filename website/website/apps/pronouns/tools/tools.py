from django.db.models import Count
from website.apps.pronouns.models import Paradigm, PronounType, Pronoun, ALIGNMENT_CHOICES

def full_repr_row(p):
    """Build a string representation of the given pronoun `p`"""
    # handle objects
    if isinstance(p, Pronoun):
        if p.pronountype.gender is None:
            return " ".join([p.pronountype.get_person_display(), p.pronountype.get_number_display()])
        else:
            return " ".join([p.pronountype.get_person_display(), p.pronountype.get_number_display(), p.pronountype.get_gender_display()])
    elif isinstance(p, PronounType):
        if p.gender is None:
            return " ".join([p.get_person_display(), p.get_number_display()])
        else:
            return " ".join([pget_person_display(), p.get_number_display(), p.get_gender_display()])
    # handle dictionary
    else:
        if p['gender'] is None:
            return " ".join([p['person'][1], p['number'][1]])
        else:
            return " ".join([p['person'][1], p['number'][1], p['gender'][1]])


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


    
def add_pronoun_ordering(pronoun_form):
    rows = {}
    for form in pronoun_form:
        row = full_repr_row(form.instance)
        rows[row] = rows.get(row, 
            dict(zip([x[0] for x in ALIGNMENT_CHOICES], [None for x in ALIGNMENT_CHOICES]))
        )
        rows[row][form.instance.pronountype.alignment] = form
        
    pronoun_form.pronoun_rows = []
    # Sort
    ptype_rows = PronounType._generate_all_rows()
    
    for row in ptype_rows:
        wanted_label = full_repr_row(row)
        found_row = False
        for label in rows:
            if wanted_label == label:
                pronoun_form.pronoun_rows.append((label, rows[label]))
                found_row = True
        assert found_row, "Unable to find expected row for Paradigm: %s" % label
    
    assert len(pronoun_form.pronoun_rows) == len(ptype_rows)
    return pronoun_form


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
            dict(zip([_[0] for _ in ALIGNMENT_CHOICES], 
                     [None for _ in ALIGNMENT_CHOICES]))
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
                    if non_zero: # at least one cell is not empty
                        pronoun_rows.append((label, cells[label]))
                else:
                    pronoun_rows.append((label, cells[label]))
        assert found_row, \
        "Unable to find expected row for Paradigm: %s - probably need to run _prefill_pronouns()" % wanted_label
    if not filter_empty_rows: 
        assert len(pronoun_rows) == len(ptype_rows)
    return pronoun_rows


def find_identicals(paradigm):
    """Find identical forms in the given list of `pronouns`"""
    identical = set()
    pronouns = paradigm.pronoun_set.annotate(entry_count=Count('entries')).exclude(entry_count=0)
    pronouns = pronouns.values_list('id', 'entries__id', 'entries__entry')
    
    for pronoun1 in pronouns:
        for pronoun2 in pronouns:
            if pronoun1[1] == pronoun2[1]:
                continue # ignore self.
                
            if pronoun1[2] == pronoun2[2]:
                # same, try to order them consistently
                if pronoun1[1] < pronoun2[1]:
                    o = (pronoun1, pronoun2)
                else:
                    o = (pronoun2, pronoun1)
                identical.add(o)
    return identical
    

def extract_rule(values):
    rule = {'one': {}, 'two': {}, 'relationship': None}
    for key, value in values.items():
        if value == '---':
            # ignore empty
            continue
        elif key == 'relationship':
            rule['relationship'] = value
        else:
            param, subset = key.split("_")
            if param in ('gender', 'person', 'alignment', 'number'):
                rule[subset][param] = value
    
    # check some things
    if rule['relationship'] is None:
        raise ValueError("Must have a relationship value")
    if len(rule['one']) == 0:
        raise ValueError("No operands set for side 1")
    if len(rule['two']) == 0:
        raise ValueError("No operands set for side two")
        
    # all good, return rule.
    return rule


