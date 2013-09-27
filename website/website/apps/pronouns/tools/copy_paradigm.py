from website.apps.pronouns.models import Paradigm


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
    mapping_pronoun = {} # dictionary of old pronouns -> new pronouns
    mapping_entry = {}   # dictionary of old entries -> new entries
    
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
        
        mapping_pronoun[old_pk] = pron
        
        assert pron.entries.count() == 0, \
            "Oops. Lexical items should not have been copied yet"
        
        # now copy the lexical items.
        # have to use the old pronoun as the new one's forgotten everything.
        for lex_obj in lexicon_set:
            old_lex_pk = lex_obj.pk
            lex_obj.pk = None # will now create new entry
            if lex_obj.language != language:
                lex_obj.language = language
            lex_obj.save()
            
            mapping_entry[old_lex_pk] = lex_obj
            
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
        obj.pronoun1 = mapping_pronoun[obj.pronoun1.pk]
        obj.pronoun2 = mapping_pronoun[obj.pronoun2.pk]
        obj.save()
    
    return newpdm