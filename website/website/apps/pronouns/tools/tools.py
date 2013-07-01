from website.apps.pronouns.models import Paradigm, Pronoun

def full_repr_row(p):
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

def short_repr_row(p):
    """Builds a short string representation of the given pronoun `p`"""
    if isinstance(p, Pronoun):
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
            dict(zip([x[0] for x in Pronoun.ALIGNMENT_CHOICES], [None for x in Pronoun.ALIGNMENT_CHOICES]))
        )
        rows[row][form.instance.alignment] = form
        
    pronoun_form.pronoun_rows = []
    # Sort
    for row in Pronoun._generate_all_rows():
        wanted_label = full_repr_row(row)
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
        label = full_repr_row(p)
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
    old = Paradigm._prefill_pronouns
    Paradigm._prefill_pronouns = lambda x: x # Unhook prefill_pronouns!
    newpdm = Paradigm.objects.create(language=language, 
                                     source=pdm.source, 
                                     editor=pdm.editor,
                                     comment="")
    
    Paradigm._prefill_pronouns = old # Reattach prefill_pronouns (YUCK)
    
    # 2. RULES: loop over rules in pdm and copy to newpdm
    for obj in pdm.rule_set.all():
        obj.pk = None # will now create new entry
        obj.paradigm = newpdm
        obj.save()
    
    # 3. PRONOUNS: loop over pronouns in pdm and COPY to newpdm
    mapping = {} # dictionary of old pronouns -> new pronouns
    
    for pron in pdm.pronoun_set.all():
        # save these for later
        old_pk = pron.pk
        # ... and this, because as soon as we change the pk on pron, then
        # it'll forget its lexical items.
        lexicon_set = pron.entries.all()       
        
        pron.pk = None # will now create new entry
        pron.paradigm = newpdm # update paradigm
        pron.save() # save, creating a new paradigm
        
        assert pron.pk != old_pk != None, \
            "Should have created a new paradigm PK"
        
        mapping[old_pk] = pron
        
        assert pron.entries.count() == 0, \
            "Oops. Lexical items should not have been copied yet"
        
        # now copy the lexical items.
        # have to use the old pronoun as the new one's forgotten everything.
        for lex_obj in lexicon_set:
            lex_obj.pk = None # will now create new entry
            if lex_obj.language != language:
                lex_obj.language = language
            lex_obj.save()
            
            # and add to new pronoun
            pron.entries.add(lex_obj)
        
        assert pron.entries.count() == len(lexicon_set), \
            "Lexicon count does not match %d, got %d" % (len(lexicon_set), pron.entries.count())
            
    assert pdm.pronoun_set.count() == newpdm.pronoun_set.count(), \
        "Something went wrong - should have the same number of pronouns in both old and new paradigms"
    
    # 4. RELATIONSHIPS: loop over relationships in pdm and copy to newpdm
    for obj in pdm.relationship_set.all():
        obj.pk = None # will now create new entry
        obj.paradigm = newpdm
        
        # update pronouns
        obj.pronoun1 = mapping[obj.pronoun1.pk]
        obj.pronoun2 = mapping[obj.pronoun2.pk]
        obj.save()
    
    return newpdm