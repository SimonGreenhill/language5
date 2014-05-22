#!/usr/bin/env python
import os
import codecs

from django.contrib.auth.models import User
from website.apps.core.models import Family, Source, Language, AlternateName
from website.apps.lexicon.models import Word, Lexicon, CognateSet, Cognate

from synonyms import SYNONYMS

REFERENCE = """
Dutton, T.E., 1970. Notes on the languages of the Rigo area of the Central district of Papua. In S. A. Wurm & D. C. Laycock, eds. Pacific Linguistic Studies in honour of Arthur Capell. Canberra: Pacific Linguistics.
"""

DATAFILE = os.path.join(os.environ['IMPORTER_DATAROOT'], '0042_dutton1970.txt')

assert os.path.isfile(DATAFILE), "Cannot find: %s" % DATAFILE

#  [+] make sure username is MalcolmRoss.
ed = User.objects.get(username="malcolm")

Dutton1970 = Source.objects.create(year="1970", author="Dutton", slug="dutton1970",
                          reference=REFERENCE, bibtex="", comment="",
                          editor=ed)

Ross2014 = Source.objects.create(year="2014", author="Ross", slug="Ross2014",
                          reference="Ross, Malcom. 2014. Personal Communication", 
                          bibtex="", comment="", editor=ed)


LANGUAGES = {}
LANGUAGES['Mulaha'] = Language.objects.create(
    language="Mulaha", 
    slug="mulaha",
    dialect=None, 
    isocode="mfw", 
    classification="Trans-New Guinea, Southeast Papuan, Kwalean",
    information="",
    editor=ed
)
LANGUAGES['Humene'] = Language.objects.create(
    language="Humene", 
    slug="humene",
    dialect=None, 
    isocode="huf", 
    classification="Trans-New Guinea, Southeast Papuan, Kwalean",
    information="",
    editor=ed
)

LANGUAGES['Kwale'] = Language.objects.create(
    language="Uare", 
    slug="uare",
    dialect=None, 
    isocode="ksj", 
    classification="Trans-New Guinea, Southeast Papuan, Kwalean",
    information="",
    editor=ed
)
AlternateName.objects.create(
    language=LANGUAGES['Kwale'], editor=ed, name="Kwale", slug="kwale"
)

LANGUAGES['*Kwalean'] = Language.objects.create(
    language="Proto-Kwalean", 
    slug="proto-kwalean",
    dialect=None, 
    isocode="", 
    classification="Trans-New Guinea, Southeast Papuan, Kwalean",
    information="",
    editor=ed
)


LANGUAGES['Maria'] = Language.objects.create(
    language="Maria", 
    slug="maria",
    dialect=None, 
    isocode="mds", 
    classification="Trans-New Guinea, Southeast Papuan, Manubaran",
    information="",
    editor=ed
)
AlternateName.objects.create(
    language=LANGUAGES['Maria'], editor=ed, name="Manubaran", slug="manubaran"
)

LANGUAGES['Bareika'] = Language.objects.create(
    language="Doromu-Koki", 
    slug="doromu-bareika",
    dialect='Bareika', 
    isocode="kqc", 
    classification="Trans-New Guinea, Southeast Papuan, Manubaran",
    information="",
    editor=ed
)
AlternateName.objects.create(
    language=LANGUAGES['Bareika'], editor=ed, name="Kokila", slug="kokila"
)

LANGUAGES['Lofaika'] = Language.objects.create(
    language="Doromu-Koki", 
    slug="doromu-lofaika",
    dialect="Lofaika", 
    isocode="kqc", 
    classification="Trans-New Guinea, Southeast Papuan, Manubaran",
    information="",
    editor=ed
)
AlternateName.objects.create(
    language=LANGUAGES['Bareika'], editor=ed, name="Koriko", slug="koriko"
)

LANGUAGES['Aramaika'] = Language.objects.create(
    language="Doromu-Koki", 
    slug="doromu-aramaika",
    dialect="Aramaika", 
    isocode="kqc", 
    classification="Trans-New Guinea, Southeast Papuan, Manubaran",
    information="",
    editor=ed
)

LANGUAGES['Maranomu'] = Language.objects.create(
    language="Maria", 
    slug="maria-maranomu",
    dialect="Maranomu", 
    isocode="mds", 
    classification="Trans-New Guinea, Southeast Papuan, Manubaran",
    information="",
    editor=ed
)
AlternateName.objects.create(
    language=LANGUAGES['Maranomu'], editor=ed, name="Didigaru", slug="didigaru"
)


LANGUAGES['Maiagolo'] = Language.objects.create(
    language="Maria", 
    slug="maria-maiagolo",
    dialect="Maiagolo", 
    isocode="mds", 
    classification="Trans-New Guinea, Southeast Papuan, Manubaran",
    information="",
    editor=ed
)
AlternateName.objects.create(
    language=LANGUAGES['Maiagolo'], editor=ed, name="Imila", slug="imila"
)


LANGUAGES['Uderi'] = Language.objects.create(
    language="Maria", 
    slug="maria-uderi",
    dialect="Uderi", 
    isocode="mds", 
    classification="Trans-New Guinea, Southeast Papuan, Manubaran",
    information="",
    editor=ed
)


LANGUAGES['*Manubaran'] = Language.objects.create(
    language="Proto-Manubaran", 
    slug="proto-manubaran",
    dialect=None, 
    isocode="", 
    classification="Trans-New Guinea, Southeast Papuan, Manubaran",
    information="",
    editor=ed
)
LANGUAGES['*Kwale-Mulaha'] = Language.objects.create(
    language="Proto-Kwale-Mulaha", 
    slug="proto-kwale-mulaha",
    dialect=None, 
    isocode="", 
    classification="Trans-New Guinea, Southeast Papuan, Kwalean",
    information="",
    editor=ed
)
LANGUAGES['*Maria'] = Language.objects.create(
    language="Proto-Maria", 
    slug="proto-maria",
    dialect=None, 
    isocode="", 
    classification="Trans-New Guinea, Southeast Papuan, Manubaran",
    information="",
    editor=ed
)

# Add all languages to Trans-New Guinea
TNG = Family.objects.get(slug='transnewguinea')
for i, lang in enumerate(LANGUAGES.values(), 1):
    lang.family.add(TNG)
    lang.save()
    print("Created Language %d: %s" % (i, lang))
    

cognates = {}
lexicon_counter = 0
with codecs.open(DATAFILE, 'rU', encoding="utf8") as handle:
    for lineid, oline in enumerate(handle.readlines(), 1):
        line = oline.strip()
        
        if len(line) == 0:
            # reset
            wslug = None
        elif line.startswith("#"):
            wslug = line[1:].strip()
            
            try:
                WObj = Word.objects.get(slug=wslug)
            except Word.DoesNotExist:
                raise ValueError("Unknown Word: %s" % wslug)
        else:
            if wslug is None:
                raise ValueError("Error on L.%d: no slug" % lineid)
            
            line = [_.strip() for _ in line.split("\t")]
            
            if len(line) not in (3, 4):
                raise ValueError("Malformed Line L.%d: %s" % (lineid, oline))
            
            # handle language
            language = line.pop(0)
            if language not in LANGUAGES:
                raise ValueError("Unknown Language on L.%d: %s" % (lineid, language))
            LObj = LANGUAGES[language]
            
            # get other fields:
            sgloss = line.pop(0)
            entry = line.pop(0)
            
            #  [+] Check cogid (cogid should be int or none)
            if len(line) == 0:
                cognate = None
            elif len(line) == 1:
                try:
                    cognate = int(line.pop())
                except ValueError:
                    raise ValueError("Malformed Cognate ID on L.%d: %s" % (lineid, line[0]))
            else:
                raise ValueError("Malformed Line on L.%d: %s" % (lineid, oline))
            
            #  [+] all *<forms> go to Ross Pers.comm. All OTHER forms go to Dutton 1970.
            if language.startswith("*"):
                SObj = Ross2014
            else:
                SObj = Dutton1970
            
            lex = Lexicon.objects.create(
                language=LObj, 
                source=SObj,
                word=WObj, 
                entry=entry, 
                source_gloss=sgloss,
                annotation='',
                editor=ed
            )
            lex.save()        
            lexicon_counter += 1
            
            print("Created Lexicon obj %4d: %040s - %s" % (lexicon_counter, LObj, entry))
            
            # temp store cognate
            if cognate is not None:
                key = (cognate, WObj)
                cognates[key] = cognates.get(key, [])
                cognates[key].append(lex)
            
            
# handle cognates
#  [+] make sure cognates are created
#  [+] Malcolm's cog.id should be saved.
cog_counter = 0
for i, key in enumerate(cognates, 1):
    cogid, WObj = key
    # TODO: figure out gloss ???
    CogSet = CognateSet.objects.create(
        protoform='',
        gloss=WObj.word,
        source=Ross2014,
        comment="MDR: %d" % cogid,
        quality='0', # unassesed
        editor=ed
    )
    CogSet.save()
    print("Created CognateSet obj %d: %s" % (i, CogSet))
    
    for m in cognates[key]:
        cog = Cognate.objects.create(lexicon=m, cognateset=CogSet, source=Ross2014, editor=ed)
        cog.save()
        cog_counter += 1
        print("  Created Cognate obj %d: %s, %s" % (cog_counter, CogSet, m))
        
    
    
    