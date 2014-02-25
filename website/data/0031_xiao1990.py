#!/usr/bin/env python
import os
import codecs
from django.contrib.auth.models import User
ed = User.objects.get(pk=1)

# import models
from website.apps.core.models import Source, Language
from website.apps.lexicon.models import Word, Lexicon, Cognate, CognateSet

S = Source.objects.get(slug="xiao-1990")

# importer sets some variables
datafiles = {
    'awa': os.path.join(os.environ['IMPORTER_DATAROOT'], 
                        '0031_xiao1990/Xiao-Awa.txt'),
    'binumarien': os.path.join(os.environ['IMPORTER_DATAROOT'], 
                        '0031_xiao1990/Xiao-Binumarien.txt'),
    'hua': os.path.join(os.environ['IMPORTER_DATAROOT'], 
                        '0031_xiao1990/Xiao-Hua.txt'),
}

cognates = {}

for lslug, lfile in datafiles.items():
    L = Language.objects.get(slug=lslug)
    with codecs.open(lfile, 'rU', encoding="utf8") as handle:
        for line in handle.readlines():
            line = line.strip().split(" ", 1)
            if len(line) == 0:
                continue
            elif len(line) == 1:
                wslug, entry = line[0], None
            elif len(line) == 2:
                wslug, entry = line
            else:
                raise ValueError("Malformed line: {} - {}".format(lfile, line))
            
            if entry is not None:
                W = Word.objects.get(slug=wslug)
                print S.slug.ljust(10), L.slug.ljust(10), W.slug.ljust(20), entry
                
                lex = Lexicon.objects.create(
                    language=L, source=S, word=W, entry=entry, editor=ed
                )

                cognates[W] = cognates.get(W, [])
                cognates[W].append(lex)

# create cognate sets.
for W, members in cognates.items():
    if len(members) > 1:
        cogset = CognateSet.objects.create(protoform="", gloss=W.word, source=S, editor=ed)
        for m in members:
            cog = Cognate.objects.create(lexicon=m, cognateset=cogset,
                                         source=S, editor=ed)
            
print("{} lexicon saved".format(
    Lexicon.objects.filter(source=S).count()
))

print("{} Cognates saved".format(
    Cognate.objects.filter(source=S).count()
))

