#!/usr/bin/env python
import os
import re
import codecs

from django.contrib.auth.models import User
from website.apps.core.models import Source, Language
from website.apps.lexicon.models import Word, Lexicon, CognateSet, Cognate

REFERENCE = """
Franklin KJ. 1975. Comments on Proto-Engan. In SA Wurm, Ed. New Guinea Area Languages and Language Study: Papuan languages and the New Guinea linguistic scene. Canberra: Pacific Linguistics, pp. 263-275.
""".strip().lstrip()

DATAFILE = os.path.join(os.environ['IMPORTER_DATAROOT'], '0033_franklin1975.txt')

LANGUAGES = {
    'KW': ['west-kewa', None],
    'KE': ['east-kewa', None],
    'KS': ['erave', None],
    'M': ['angal', None],
    'MN': ['angal', None],
    'MS': ['angal-enen', None],
    'MW': ['angal-heneng', None],
    'S': ['samberigi', None],
    'E': ['enga', None],
    'H': ['huli', None],
    'I': ['ipili', None],
    'W': ['wiru', None],
    'F': ['fasu', None],
}


IS_WORD = re.compile(r"""^\w+.*$""")
IS_ENTRY = re.compile(r"""^\s+(\w{1,2})\s+(.*)$""")
# get editor
ed = User.objects.get(pk=1)

SObj = Source.objects.create(year="1975", author="Franklin", slug="franklin1975",
                          reference=REFERENCE, bibtex="", comment="",
                          editor=ed)

# NOTE
# comments are | 
# everything tagged with "K" should be given to ["KW", "KE", "KS"]

from tools import get_latest_words
wordslugs = get_latest_words()

entries = []

with codecs.open(DATAFILE, 'rU', encoding="utf8") as handle:
    word, cogset = None, None
    for line in handle.readlines():
        if IS_WORD.match(line):
            slug = line.strip().replace(" ", "-")
            if slug not in wordslugs:
                raise ValueError("Unknown Slug: {}".format(slug))
            
            # Get word
            WObj = Word.objects.get(slug=slug)
            
            # Get Cognate Set
            CogSet = CognateSet.objects.create(
                protoform="",
                gloss=slug,
                source=SObj,
                comment="",
                quality='1', # published
                editor=ed
            )
            CogSet.save()
            print(u"Created Cogset: {}".format(CogSet))
        
        elif IS_ENTRY.match(line):
            token, entry = IS_ENTRY.findall(line)[0]
            if "|" in entry:
                entry, comment = entry.split("|")
                entry, comment = entry.strip(), comment.strip()
            else:
                comment = ""
            
            if token == 'K':
                langs = ['KW', 'KE', 'KS']
            else:
                langs = [token]
            
            if entry.startswith("["):
                is_cognate = False
                entry = entry.lstrip('[').strip(']')
            else:
                is_cognate = True
            
            assert '[' not in entry
            assert ']' not in entry
            
            
            # get Language
            for ltoken in langs:
                
                lslug, LObj = LANGUAGES.get(ltoken)
                if LObj is None: # rudimentary caching
                    LObj = Language.objects.get(slug=lslug)
                    LANGUAGES[ltoken] = [lslug, LObj]
                
                # create lexicon
                lex = Lexicon.objects.create(
                    language=LObj, 
                    source=SObj,
                    word=WObj, 
                    entry=entry, 
                    annotation=comment, 
                    editor=ed
                )
                lex.save()
                print(u"Created Lexicon: {}".format(lex))
                
                # add to cognate set
                if is_cognate:
                    cog = Cognate.objects.create(lexicon=lex, cognateset=CogSet, source=SObj, editor=ed)
                    cog.save()
                    print(u"Created Cognate: {}".format(cog))
                
            