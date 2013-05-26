#!/usr/bin/env python
import codecs

from django.contrib.auth.models import User

# import models
from website.apps.core.models import Source, Language, AlternateName, Family
from website.apps.lexicon.models import Lexicon, Word

# importer sets some variables
import os
#print os.environ['IMPORTER_SITEROOT'] # the site root
#print os.environ['IMPORTER_FILENAME'] # the filename currently being imported

bibtex = """@book{Foley1986,
address = {Cambridge},
author = {Foley, William A},
publisher = {Cambridge University Press},
title = {The Papuan languages of New Guinea},
year = {1986}
}
""".strip()

reference = """Foley, W.A., 1986. The Papuan languages of New Guinea, Cambridge: Cambridge University Press.""".strip()


def reader(filename):
    entries = []
    with codecs.open(filename, 'rU', encoding="UTF-8") as handle:
        for line in handle.readlines():
            line = line.strip()
            if line.startswith("#"):
                continue
            elif len(line) == 0:
                continue
            else:
                word, entry = line[0:13].strip(), line[13:].strip()
                if len(entry) > 0:
                    entries.append((word, entry))
    return entries



# get editor
ed = User.objects.get(pk=1)

s = Source.objects.create(year=1986, author="Foley", slug="foley1986",
                          reference=reference, bibtex=bibtex, comment="",
                          editor=ed)
s.save()


LANGUAGES = {
    'Angoram.txt': Language.objects.create(editor=ed,
        language = "Angoram",
        slug = "angoram",
        isocode = "aog",
        classification = "Ramu-Lower Sepik, Lower Sepik, Angoram"
    ),
    
    'Chambri.txt': Language.objects.create(editor=ed,
        language = "Chambri",
        slug = "chambri",
        isocode = "can",
        classification = "Ramu-Lower Sepik, Lower Sepik, Chambri"
    ),
    
    'Karawari.txt': Language.objects.create(editor=ed,
        language = "Tabriak",
        slug = "tabriak",
        isocode = "tzx",
        classification = "Ramu-Lower Sepik, Lower Sepik, Karawari"
    ),
    # alt name Karawari

    'Yimas.txt': Language.objects.create(editor=ed,
        language = "Yimas",
        slug = "yimas",
        isocode = "yee",
        classification = "Ramu-Lower Sepik, Lower Sepik, Karawari"
    ),


    'Murik-Kopar.txt': Language.objects.create(editor=ed,
        language = "Kopar",
        slug = "kopar",
        isocode = "xop",
        classification = "Ramu-Lower Sepik, Lower Sepik, Nor"
    ),
    'Murik.txt': Language.objects.create(editor=ed,
        language = "Murik",
        slug = "murik",
        isocode = "mtf",
        classification = "Ramu-Lower Sepik, Lower Sepik, Nor"
    ),
    'Proto-Lower-Sepik.txt': Language.objects.create(editor=ed,
        language = "Proto-Lower-Sepik",
        slug = "proto-lower-sepik",
        isocode = "",
        classification = "Ramu-Lower Sepik, Lower Sepik"
    ),
}
# add some altnames
AlternateName.objects.create(editor=ed, 
    language=LANGUAGES['Karawari.txt'], name="Karawari", slug="karawari"
)

# add families
family = Family.objects.get(slug="lowersepikramu")
for langobj in LANGUAGES.values():
    langobj.family.add(family)


# create languages
FILEDIR = os.path.join(os.environ["IMPORTER_DATAROOT"], 'Foley1986')

for filename in os.listdir(FILEDIR):
    if filename.endswith('.txt'):
        print(filename)
        lang = LANGUAGES.get(filename)
        
        content = reader(os.path.join(FILEDIR, filename))
        for word, entry in content:
            print(" %s %s" % (word.ljust(20), entry))
            
            wslug = word.replace(" ", "-")
            
            try:
                w = Word.objects.get(slug=wslug)
            except:
                w = Word.objects.create(slug=wslug, word=word, editor=ed)
            
            l = Lexicon.objects.create(
                editor=ed,
                source=s,
                language=lang,
                entry=entry,
                word=w
            )