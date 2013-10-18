#!/usr/bin/env python
import os
import codecs

from django.contrib.auth.models import User

# import models
from website.apps.core.models import Source, Language, Family
from website.apps.lexicon.models import Word, Lexicon

# importer sets some variables
# import os
# print os.environ['IMPORTER_SITEROOT'] # the site root
# print os.environ['IMPORTER_DATAROOT'] # the root of the data dir
# print os.environ['IMPORTER_FILENAME'] # the filename currently being imported

reference = """
Kamholz, D. 2012. The Keuw isolate: Preliminary materials and classification. Language & Linguistics in Melanesia. 2012: 1. 243-268.
"""

# get editor
ed = User.objects.get(pk=1)
# create source
S = Source.objects.create(year=2012, author="Kamholz", slug="kamholz2012",
                          reference=reference, bibtex="", comment="",
                          editor=ed)
S.save()

# create language
L = Language.objects.create(language="Keuw", 
                            dialect=None,
                            slug="keuw",
                            isocode="khh",
                            classification="East Geelvink Bay",
                            editor=ed
                            )
L.save()

# Add to Family
f = Family.objects.get(slug="eastgeelvinkbay")
f.language_set.add(L)
f.save()

# check datafile -
filename = os.path.join(os.environ['IMPORTER_DATAROOT'], '0008_keuw.dat')
assert os.path.isfile(filename), "Unable to find datafile: %s!" % filename

# preload all known words
WORDS = {}
for W in Word.objects.all():
    WORDS[W.slug] = W
print("Found {0} Words...".format(len(WORDS)))

# Loop through...
missing = 0

good = []
with codecs.open(filename, 'rU', encoding='utf8') as handle:
    for line in handle.readlines():
        line = line.strip()
        if len(line) == 0:
            continue
            
        try:
            english, keuw = [_.strip() for _ in line.split("\t")]
        except:
            raise ValueError("Invalid: %r" % line)
        
        # make sluglike things
        eng = english.replace(" ", "-").replace("?", "").replace(".", "")
        eng = eng.replace("(", "").replace(")", "").replace(",", "")
        toeng = toeng = 'to-%s' % eng
        
        if "(cid:" in keuw:
            raise ValueError(u'Error! : %s - %s' % (eng, keuw))
        
        if eng in WORDS:
            W = WORDS[eng]
        elif toeng in WORDS:
            W = WORDS[toeng]
        else:
            print("Creating Word: {0} <{1}> <{2}>".format(english, eng, toeng))
            W = Word.objects.create(
                    word=english, 
                    slug=eng,
                    full="", 
                    comment="",
                    quality="",
                    editor=ed)
            W.save()
            # add slug to wordslugs list for future entries
            WORDS[W.slug] = W
            
        e = Lexicon.objects.create(
                                language=L, 
                                source=S,
                                word=W, 
                                entry=keuw, 
                                annotation="",
                                editor=ed
        )
        e.save()
        print("\tCreating Lexicon: {0} = {1}".format(W, e))
