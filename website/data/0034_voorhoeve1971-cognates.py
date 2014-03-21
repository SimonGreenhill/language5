#!/usr/bin/env python
from django.contrib.auth.models import User

# import models
from website.apps.core.models import Source
from website.apps.lexicon.models import Word, Lexicon, CognateSet, Cognate

V71 = Source.objects.get(slug="voorhoeve-1971")

# get editor
ed = User.objects.get(pk=1)

# cognates are by word/semantic slot.
cognates = {}



for lex in V71.lexicon_set.all():
    if lex.annotation:
        cog, annot = None, []
        for chunk in lex.annotation.split(","):
            chunk = chunk.strip()
            if chunk == '-':
                continue
            else:
                try:
                    cog = int(chunk)
                except ValueError:
                    annot.append(chunk)
        
        annot = ", ".join(annot)
        annot = annot.strip()
        
        if cog is not None:
            #print cog, ':', lex.annotation.ljust(20), '->', annot
            cognates[lex.word] = cognates.get(lex.word, {})
            
            if cog not in cognates[lex.word]:
                cogset = CognateSet.objects.create(
                    protoform="",
                    gloss=lex.word.word,
                    source=V71,
                    comment="",
                    quality='1', # published
                    editor=ed
                )
                cogset.save()
                print(u"Created Cogset: {}".format(cogset))
                cognates[lex.word][cog] = cogset
            else:
                cogset = cognates[lex.word][cog]
            
            # update
            CO = Cognate.objects.create(lexicon=lex, cognateset=cogset, source=V71, editor=ed)
            print(u"Created Cognate: {}".format(CO))
        
        if lex.annotation != annot:
            print(u"Updated Lex # {}: {} -> {}".format(lex.id, lex.annotation, annot))
            lex.annotation = annot
            lex.save()
            
            