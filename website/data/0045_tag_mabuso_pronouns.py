#!/usr/bin/env python
#coding=utf-8

import os
import re
import reversion
from website.apps.core.models import Source
from website.apps.lexicon.models import Word, Lexicon

S = Source.objects.get(slug="zgraggen-1980-mabuso")

words = {
    'I-gen-P1S': 'my',
    'thou-genitive-P2S': 'your-sg',
    'he-gen-P3S': 'his',
    'we-gen': 'our',
    'we-two-gen': 'our-dual',
    'ye-gen': 'your-pl',
    'you-two-gen': 'your-pl-dual',
    'they-two-gen': 'their-dual',
    'they-gen-P3P': 'their',
}

for wslug in words.values():
    W = Word.objects.get(slug=wslug)
    lexicon = Lexicon.objects.all().filter(source=S).filter(word=W)
    for lex in lexicon:
        if lex.annotation is not None:
            raise ValueError, "Lexicon already has annotation."
        
        with reversion.create_revision():
            lex.annotation = 'gen.'
            lex.save()
        print lex.id, lex.source_gloss, lex.annotation
    print