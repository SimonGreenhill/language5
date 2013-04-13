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
    rows = {}
    for p in pronoun_set:
        row = repr_row_instance(p)
        rows[row] = rows.get(row, 
            dict(zip([x[0] for x in Pronoun.ALIGNMENT_CHOICES], [None for x in Pronoun.ALIGNMENT_CHOICES]))
        )
        rows[row][p.alignment] = p
    
    pronoun_rows = []
    # Sort
    for row in Pronoun._generate_all_rows():
        wanted_label = "%s %s %s" % (row['person'][1], row['number'][1], row['gender'][1]) 
        found_row = False
        for label in rows:
            if wanted_label == label:
                if filter_empty_rows:
                    non_zero = 0
                    for cell, value in rows[label].items():
                        if value is not None and len(value.form) > 0:
                            non_zero += 1
                    if non_zero:
                        pronoun_rows.append((label, rows[label]))
                else:
                    pronoun_rows.append((label, rows[label]))
                found_row = True
        assert found_row, "Unable to find expected row for Paradigm: %s" % label
    
    if not filter_empty_rows: 
        assert len(pronoun_rows) == len(Pronoun._generate_all_rows())
    return pronoun_rows
