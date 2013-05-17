from website.apps.pronouns.models import Pronoun

def repr_row(p):
    """Build a string representation of the given pronoun `p`"""
    # handle objects
    if isinstance(p, Pronoun):
        if p.gender is None:
            return " ".join([p.get_person_display(), p.get_number_display()])
        else:
            return " ".join([p.get_person_display(), p.get_number_display(), p.get_gender_display()])
    # handle dictionary
    else:
        if p['gender'] is None:
            return " ".join([p['person'][1], p['number'][1]])
        else:
            return " ".join([p['person'][1], p['number'][1], p['gender'][1]])

    
def add_pronoun_ordering(pronoun_form):
    rows = {}
    for form in pronoun_form:
        row = repr_row(form.instance)
        rows[row] = rows.get(row, 
            dict(zip([x[0] for x in Pronoun.ALIGNMENT_CHOICES], [None for x in Pronoun.ALIGNMENT_CHOICES]))
        )
        rows[row][form.instance.alignment] = form
        
    pronoun_form.pronoun_rows = []
    # Sort
    for row in Pronoun._generate_all_rows():
        wanted_label = repr_row(row)
        found_row = False
        for label in rows:
            if wanted_label == label:
                pronoun_form.pronoun_rows.append((label, rows[label]))
                found_row = True
        assert found_row, "Unable to find expected row for Paradigm: %s" % label
    
    assert len(pronoun_form.pronoun_rows) == len(Pronoun._generate_all_rows())
    return pronoun_form


def add_pronoun_table(pronoun_set, filter_empty_rows=True):
    """Construct a table for the given pronoun set
    
    `filter_empty_rows` - leave out the rows that are empty.
    """
    # loop over the pronouns we've been given and fill a table of the cells.
    cells = {}
    for p in pronoun_set:
        label = repr_row(p)
        # get row or set it to (A, None), (S, None), (O, None), (P, None)
        # i.e. empty placeholders for each different ALIGNMENT
        cells[label] = cells.get(label, 
            dict(zip([_[0] for _ in Pronoun.ALIGNMENT_CHOICES], 
                     [None for _ in Pronoun.ALIGNMENT_CHOICES]))
        )
        # Save the pronoun into the right row/alignment cell.
        cells[label][p.alignment] = p
    
    # Now do the sorting of the table *rows*
    pronoun_rows = []
    # Sort
    for row in Pronoun._generate_all_rows():
        wanted_label = repr_row(row)
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
                        if value is not None and len(value.form) > 0:
                            non_zero += 1
                    if non_zero: # at least one cell is not empty
                        pronoun_rows.append((label, cells[label]))
                else:
                    pronoun_rows.append((label, cells[label]))
        assert found_row, "Unable to find expected row for Paradigm: %s - probably need to run _prefill_pronouns()" % wanted_label
            
    if not filter_empty_rows: 
        assert len(pronoun_rows) == len(Pronoun._generate_all_rows())
    return pronoun_rows


def find_identicals(pronouns):
    """Find identical forms in the given list of `pronouns`"""
    identical = set()
    for p1 in pronouns:
        if p1.form == '':
            # ignore empties.
            continue
            
        for p2 in pronouns:
            if p2.form == '':
                # ignore empties
                continue
            elif p1 == p2:
                # ignore self
                continue
            elif p1.form == p2.form:
                identical.add(tuple(sorted([p1,p2])))
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
    
    



def copy_paradigm(pdm, language):
    """Copies the paradigm `pdm` to a new paradigm for `language`"""
    # 1. create new paradigm
    newpdm = Paradigm.objects.create(language=language, 
                                     source=pdm.source, 
                                     editor=pdm.editor,
                                     comment="")
    
    # 2. loop over pronouns in pdm and COPY to newpdm
    #for p in pronouns
    
    
    # 3. loop over rules in pdm and copy to newpdm
    
    # 4. loop over relationships in pdm and copy to newpdm
    
