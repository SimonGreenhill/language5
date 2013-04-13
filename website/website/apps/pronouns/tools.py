from website.apps.pronouns.models import Pronoun

def repr_row(p):
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
