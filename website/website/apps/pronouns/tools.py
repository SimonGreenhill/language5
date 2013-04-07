from website.apps.pronouns.models import Pronoun

def repr_row_instance(p):
    return "%s %s %s" % (p.get_person_display(), p.get_number_display(), p.get_gender_display())

def add_pronoun_ordering(pronoun_form):
    rows = {}
    for form in pronoun_form:
        row = repr_row_instance(form.instance)
        rows[row] = rows.get(row, 
            dict(zip([x[0] for x in Pronoun.ALIGNMENT_CHOICES], [None for x in Pronoun.ALIGNMENT_CHOICES]))
        )
        rows[row][form.instance.alignment] = form
        
    pronoun_form.pronoun_rows = []
    # Sort
    for row in Pronoun._generate_all_rows():
        wanted_label = "%s %s %s" % (row['person'][1], row['number'][1], row['gender'][1]) 
        found_row = False
        for label in rows:
            if wanted_label == label:
                pronoun_form.pronoun_rows.append((label, rows[label]))
                found_row = True
        assert found_row, "Unable to find expected row for Paradigm: %s" % label
    
    assert len(pronoun_form.pronoun_rows) == len(Pronoun._generate_all_rows())
    return pronoun_form
