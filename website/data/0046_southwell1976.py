#!/usr/bin/env python
#coding=utf-8
import os
import re
import codecs
from django.contrib.auth.models import User
from website.apps.core.models import Source, Language
from website.apps.lexicon.models import Lexicon, Word

from synonyms import SYNONYMS, find_synonym

FILENAME = os.environ['IMPORTER_FILENAME'].replace(".py", ".txt")
IS_WHITESPACE = re.compile(r"""\s+""")


# get editor
ed = User.objects.get(pk=1)

SObj = Source.objects.create(
    year=1976, 
    author="Southwell", 
    slug="southwell1976",
    reference="Southwell (1976). Komba Dialect Survey.", 
    bibtex="", 
    comment="",
    editor=ed)

LANGUAGES = {}
LANGUAGES['1a'] = Language.objects.create(
    language="Komba", 
    slug="komba-gwama-north",
    dialect="Gwama River (North)", 
    isocode="kpf", 
    classification="Trans-New Guinea, Finisterre-Huon, Huon, Western",
    information="",
    editor=ed
)
LANGUAGES['1b'] = Language.objects.create(
    language="Komba", 
    slug="komba-gwama-south",
    dialect="Gwama River (South)", 
    isocode="kpf", 
    classification="Trans-New Guinea, Finisterre-Huon, Huon, Western",
    information="",
    editor=ed
)
LANGUAGES['2'] = Language.objects.create(
    language="Komba", 
    slug="komba-anda",
    dialect=u"Ândâ River", 
    isocode="kpf", 
    classification="Trans-New Guinea, Finisterre-Huon, Huon, Western",
    information="",
    editor=ed
)
LANGUAGES['3'] = Language.objects.create(
    language="Komba", 
    slug="komba-puleng",
    dialect="Puleng River", 
    isocode="kpf", 
    classification="Trans-New Guinea, Finisterre-Huon, Huon, Western",
    information="",
    editor=ed
)

# create a few words
Word.objects.create(
    word = "blossom",
    slug = "blossom",
    full = "",
    editor = ed
)
Word.objects.create(
    word = "death adder",
    slug = "death-adder",
    full = "",
    editor = ed
)
Word.objects.create(
    word = "orphan",
    slug = "orphan",
    full = "",
    editor = ed
)
Word.objects.create(
    word = "seat",
    slug = "seat",
    full = "",
    editor = ed
)
SYNONYMS.update({
    'mine': 'my',
    'yours': 'your-sg',
    
    
})


assert os.path.isfile(FILENAME), "Unable to find:%s" % FILENAME
counter = 0
with codecs.open(FILENAME, 'rU', encoding="utf8") as handle:
    for line in handle.readlines():
        line = line.strip()
        if len(line) == 0:
            continue
        line = IS_WHITESPACE.split(line, 2)
        token = line.pop(0)
        assert token in ('0', '1a', '1b', '2', '3')
        
        wordslug = line.pop(0).lower()
        if find_synonym(wordslug):
            wordslug = find_synonym(wordslug)
        
        try:
            WObj = Word.objects.get(slug=wordslug)
        except Word.DoesNotExist:
            print("ERROR: Unknown word: %s" % wordslug)
            #raise Word.DoesNotExist("Unknown word: %s" % wordslug)
            
        
        assert len(line) == 1, 'Error: %r' % line
        line = line.pop()
        if '//' in line:
            entry, comment = [_.strip() for _ in line.split("//")]
        else:
            entry, comment = line.strip(), ""
        
        
        if token == '0':
            langs = LANGUAGES.keys()
        else:
            langs = [token]
        
        sgloss = comment if len(comment) else wordslug.replace("-", " ")
        
        for t in langs:
            LObj = LANGUAGES.get(t)
            lex = Lexicon.objects.create(
                language=LObj, 
                source=SObj,
                word=WObj, 
                entry=entry, 
                phon_entry=u"", 
                annotation=comment,
                loan="", 
                source_gloss=sgloss,
                editor=ed
            )
            lex.save()
            counter += 1
            print("Created %d. %s - %s - %s (%s)" % (
                counter, LObj.slug, WObj.slug, entry, sgloss
            ))

