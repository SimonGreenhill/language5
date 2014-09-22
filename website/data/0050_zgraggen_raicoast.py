#!/usr/bin/env python
#coding=utf-8

import os
import re
import codecs
from django.contrib.auth.models import User
from website.apps.core.models import Family, Source, Language, AlternateName
from website.apps.lexicon.models import Word, Lexicon, CognateSet, Cognate

from synonyms import SYNONYMS, find_synonym

FAIL = True # Fail on errors or not.

DIRNAME = os.path.join(os.environ['IMPORTER_DATAROOT'], '0050_zgraggen_raicoast')
REFERENCE = "Z'graggen, J.A., 1980. A comparative word list of the Rai Coast Languages, Madang Province, Papua New Guinea, Canberra: Pacific Linguistics."

IS_DIGIT = re.compile(r"\d{1-4}+")

# Specific synonyms for this dataset
SYNONYMS.update({
    'PossessiveMarker': 'possessive-marker',
    'iron-axe': 'axe-iron',
    'stone-axe': 'axe',
    
    'older-same-sex-sibling': 'sibling-same-sex-older',
    'young-same-sex-sibling': 'sibling-same-sex-younger',
    'sibling-different-sex-older': 'sibling-opposite-sex-older',
    'sibling-different-sex-younger': 'sibling-opposite-sex-younger',
    
    'clay-pot': 'pot',
    'to-sit-down': 'to-sit',
    'to-stand-up': 'to-stand',
    'to-fall-tree': 'fell-tree',
    'to-fill-up-water': 'to-fill',
    'to-look-for': 'to-look',
    'to-make': 'to-do-make',
    'to-break-across': 'to-break',
    
    'to-fly-v': 'to-fly',
    'to-swell-up': 'to-swell',
    'to-talk-itr': 'to-talk',
    'to-talk-tr': 'to-talk',
    'to-watch-itr': 'to-watch',
    'to-wash-tr': 'to-wash',
    'to-carry-on-back': 'to-carry',
    'to-blow-on-fire': 'to-blow',
    'to-fell': 'fell-tree',
    'spear-a': 'spear-n',
    'spear-b': 'fish-spear',
    'alangalang-grass': 'kunai',
    'inside': 'in',
    'potato': 'sweet-potato',
    'taro-singapore': 'singapore-taro',
    'gstring': 'g-string',
    
    '1sg-gen': 'my',
    '1sg-obj': 'me',
    '1sg-poss': 'my',
    
    '2sg-gen': 'your-sg',
    '2sg-obj': 'you-o2s',
    '2sg-poss': 'your-sg',

    '3sg-gen': 'his',
    '3sg-obj': 'him-her-it',
    '3sg-poss': 'his',
    
    '1pl-gen': 'our',
    '1pl-obj': 'us',
    '1pl-poss': 'our',
    
    '2pl-obj': 'you-pl-o2p',
    '2pl-gen': 'your-pl',
    '2pl-poss': 'your-pl',
    
    '3pl-gen': 'their',
    '3pl-obj': 'them',
    '3pl-poss': 'theirs',   ## CREATE
})

LANGUAGES = {
    'B1 Sinsauru': 'sinsauru',
    'B2 Asas': 'asas',
    'B3 Sausi': 'sausi',
    'B4 Koromu': 'kesawai',
    'B5 Dumpu': 'watiwa',
    'B6 Arawum': 'arawum',
    'B7 Kolom': 'migum',
    'B8 Suroi': 'siroi',
    'B9 Lemio': 'lemio',
    'B10 Pulabu': 'pulabu',
    'B11 Yabong': 'yabong',
    'B12 Ganglau': 'ganglau',
    'B13 Saep': 'saep',
    'B14 Usino': 'sop',
    'B15 Sumau': 'sumau',
    'B16 Urigina': 'urigina',
    'B17 Danaru': 'danaru',
    'B18 Usu': 'uya',
    'B19 Erima': 'ogea',
    'B20 Deduela': 'uyajitaya',
    'B21 Kwato': 'waube',
    'B22 Rerau': 'rerau',
    'B23 Jilim': 'jilim',
    'B24 Yangulam': 'yangulam',
    'B25 Bom': 'anjam',
    'B26 Male': 'male',
    'B27 Bongu': 'bongu',
    'B28 Songum': 'sam',
}

ERROR_COUNT = 0
def print_or_raise(message, fail):
    global ERROR_COUNT
    if fail:
        print("\n"*3)
        raise ValueError(message)
    else:
        ERROR_COUNT += 1
        print(u'%d: %s' % (ERROR_COUNT, message))
    

def clean(w):
    w = w.replace(u"ˀ", u"ʔ")
    return w
    

def get_filenames(dir):
    # get sorting 
    filenames = []
    for f in os.listdir(dir):
        token = f.split("-")[0].strip("a").strip("b")
        try:
            token = int(token)
        except:
            token = 9999
        filenames.append((token, f))
    return [f[1] for f in sorted(filenames)]


def get_wordslug(filename):
    # handles the special cases in wordslugs 
    # (at the moment, just arrow words):
    special = {
        '196a': 'arrow',
        '196b': 'arrow-pronged',
        '196c': 'arrow-barred',
        '196d': 'arrow-hooked',
    }
    
    filename = os.path.splitext(filename)[0]
    header, filename = filename.split("-", 1)
    # handle special cases..
    if header in special:
        return special[header]
    
    filename = filename.replace(" ", "-").replace("(", "").replace(")", "")
    filename = filename.strip()
    if find_synonym(filename):
        return find_synonym(filename)
    return filename

def get_sourcegloss(filename):
    special = {
        '196a': 'arrow',
        '196b': 'arrow-pronged',
        '196c': 'arrow-barred',
        '196d': 'arrow-hooked',
    }
    filename = os.path.splitext(filename)[0]
    header, filename = filename.split("-", 1)
    # handle special cases..
    if header in special:
        return special[header]
    else:
        return filename


def standardise_tabs(line):
    pop = [_ for _ in line.split("\t") if len(_.strip()) > 0]
    assert len(pop) in (2, 3, 4), "Malformed: %s" % line
    return "\t".join(pop)


def process_cognate(cognates):
    identified_cogs = []
    for cognate in cognates.split(","):
        if '?' in cognate:
            continue
        try:
            identified_cogs.append(int(cognate))
        except:
            raise ValueError(u"Cogset Error: %s" % cognate)
    
    if len(identified_cogs) == 0:
        return None
    return identified_cogs


def readfile(filename):
    records = []
    with codecs.open(filename, 'rU', encoding="utf8") as handle:
        for oline in handle.readlines():
            line = oline.strip()
            if len(line) == 0:
                continue
            if line == '*':
                raise ValueError("Bad Line: [*]")
            
            if line.strip().endswith("?"):
                raise ValueError("Questionable Entry: %s" % line[0:40])
            
            try:
                line = standardise_tabs(line.strip())
            except AssertionError:
                raise ValueError("Tab Standardise Error: %s..." % line[0:30])
            
            line = [_.strip() for _ in line.split("\t")]
            for _ in line:
                if ' ' * 3 in _:
                    raise ValueError(u"Dodgy line: %s..." % oline[0:30])
            
            language, sgloss = line.pop(0), line.pop(0)
            
            assert language in LANGUAGES, 'Invalid language: %s' % language
            
            if len(line):
                entry = line.pop(0)
                assert not IS_DIGIT.findall(entry), u"Cognate in Entry? %s" % oline
            else:
                entry = None
            
            if len(line):
                try:
                    cogset = process_cognate(line.pop(0))
                except ValueError as e:
                    print filename, repr(e)
                    raise ValueError(u"Cognate Error: %s" % e)
            else:
                cogset = None
            
            if len(line):
                raise ValueError("Remainder: '%s'" % "/".join(line))
            
            if entry:
                for e in entry.split(","):
                    e = clean(e.strip())
                    if len(language) and e:
                        records.append((language, e, sgloss, cogset))
    return records


assert os.path.isdir(DIRNAME), "Cannot find: %s" % DIRNAME


ed = User.objects.get(username="malcolm")

Word.objects.create(
    word="theirs (pronoun p:3p)",
    slug="theirs",
    full="",
    editor=ed
)


# forgot this one in 0032_zgraggen_languages.py
AlternateName.objects.create(
    language=Language.objects.get(slug="kesawai"), 
    editor=ed,
    name="Koromu", 
    slug="korumu"
)

Zgraggen = Source.objects.get(slug="zgraggen-1980-raicoast")
Ross2014 = Source.objects.get(slug="Ross2014")

# check languages
l2 = {}
for l in LANGUAGES:
    l2[l] = Language.objects.get(slug=LANGUAGES[l])
LANGUAGES = l2

all_cognates = {}
lex_counter = 0
for filename in get_filenames(DIRNAME):
    if filename.endswith('.txt'):
        try:
            wslug = get_wordslug(filename)
        except:
            print_or_raise(u"%s: Bad filename" % filename.ljust(20), FAIL)
        
        try:
            WObj = Word.objects.get(slug=wslug)
        except Word.DoesNotExist:
            print_or_raise(u"%s: Unknown WordSlug: %s" % (filename.ljust(20), wslug), FAIL)
            
        try:
            content = readfile(os.path.join(DIRNAME, filename))
        except Exception, e:
            print_or_raise(u"%s: %s" % (filename.ljust(20), e), FAIL)
            
        if len(content) < 3:
            print_or_raise("%s: Small file" % filename.ljust(20), FAIL)
        
        # override source_gloss 
        source_gloss = get_sourcegloss(filename)
        for l, entry, sgloss, cognates in content:
            LObj = LANGUAGES[l]
            lex = Lexicon.objects.create(
                language=LObj,
                word=WObj,
                source=Zgraggen,
                entry=entry,
                source_gloss=source_gloss,
                editor=ed
            )
            lex_counter += 1
            print(" %5d created %4d. %20s  %20s %s" % (lex_counter, lex.id, lex.entry, lex.source_gloss, cognates))
            
            if cognates is not None:
                for cognate in cognates:
                    key = (cognate, WObj)
                    all_cognates[key] = all_cognates.get(key, [])
                    all_cognates[key].append(lex)


# Handle cognates
cog_counter, cset_counter = 0, 0
for key in all_cognates:
    cogid, WObj = key
    try:
        CogSet = CognateSet.objects.filter(comment="MDR: %d" % cogid)[0]
        print("Found CognateSet: %d: %s" % (CogSet.id, CogSet.comment))
    except (CognateSet.DoesNotExist, IndexError):
        CogSet = CognateSet.objects.create(
            protoform='',
            gloss=WObj.word,
            source=Ross2014,
            comment="MDR: %d" % cogid,
            quality='0', # unassesed
            editor=ed
        )
        CogSet.save()
        cset_counter += 1
        print("Created CognateSet obj %d: %s" % (CogSet.id, CogSet.comment))
        
    for m in all_cognates[key]:
        cog = Cognate.objects.create(lexicon=m, cognateset=CogSet, source=Ross2014, editor=ed)
        cog.save()
        cog_counter += 1
        print(" %5d: %s << %s" % (cog_counter, CogSet, m))
        
        
print("\n\n")
print("========================================")
print("Created %d Lexical Items" % lex_counter)
print("Created %d Cognate Sets" % cset_counter)
print("Created %d Cognates" % cog_counter)
