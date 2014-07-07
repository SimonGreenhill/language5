#!/usr/bin/env python
#coding=utf-8

import os
import re
import codecs
from django.contrib.auth.models import User
from website.apps.core.models import Family, Source, Language, AlternateName
from website.apps.lexicon.models import Word, Lexicon, CognateSet, Cognate

from synonyms import SYNONYMS, find_synonym

DIRNAME = os.path.join(os.environ['IMPORTER_DATAROOT'], '0044_zgraggen_nadelbert')
REFERENCE = "Z'graggen, J.A., 1980. A comparative word list of the Northern Adelbert Range Languages, Madang Province, Papua New Guinea, Canberra: Pacific Linguistics."

IS_DIGIT = re.compile(r"\d{1-4}+")

# Specific synonyms for this dataset
SYNONYMS.update({
    # 'axe-iron': 'axe-iron',
    # 'NegationMarker': 'negation-marker',
    # 'inside': 'in',
    # 'to-chop-cut-down': 'to-chop',
    
    'lightening': 'lightning',
    'flyv': 'to-fly',
    'flyn': 'fly-sp',
    'PossessiveMarker': 'possessive-marker',
    'male-of-animals': 'male',
    'female-of-animals': 'female',
    'spear': 'spear-n',
    'spear-fish-spear': 'fish-spear',
    'calf-of-leg': 'calf',
    'fight-hit': 'to-fight',
    'tie': 'to-tie',
    'fasten': 'to-fasten',
    'potato': 'sweet-potato',
    'stone-axe': 'axe',
    
    'I-1st-person-singular': 'i',
    'I-gen': 'my',
    'I-vo': 'me',
    
    'thou-free': 'you',
    'thou-gen': 'your-sg',
    'thou-vo': 'you-o2s',
    
    'he-free': 'he-she',
    'he-gen': 'his',
    'he-vo': 'him-her-it',
    
    'ye-free': 'you-pl',
    'ye-gen': 'your-pl',
    'ye-vo': 'you-pl-o2p',
    
    'they-free': 'they',
    'they-gen': 'their',
    'they-vo': 'them',
    
    'we-free': 'we',
    'we-genitive': 'our',
    'we-vo': 'us',
    
    'he-possessive': 'his',
    'thou-possessive': 'your-sg',
    '1st-sg-poss': 'my',
    'ye-poss': 'your-pl',
    'they-poss': 'their',
    'we-poss': 'our',
    
    
    
    
})

LANGUAGES = {
    "D1 Bargam": 'bargam',
    "E1 Dimir": 'gavak',
    "E2 Malas": 'malas',
    "E3 Bunabun": 'brem',
    "E4 Korak": 'korak',
    "E5 Waskia": 'waskia',
    "F1 Pay": 'mala',
    "F2 Pila": 'maia-pila',
    "F3 Maia": 'maia-saki',
    "F4 Tani": 'miani',
    "F5 Mauwake": 'mauwake',
    "F6 Bepour": 'bepour',
    "F7 Moere": 'moere',
    "F8 Kowaki": 'kowaki',
    "F9 Mawak": 'mawak',
    "F10 Hinihon": 'pamosu',
    "F11 Musar": 'musar',
    "F12 Wanambre": 'wanambre',
    "F13 Koguman": 'kobol',
    "F14 Abasakur": 'pal',
    "F15 Usan": 'usan',
    "F16 Yaben": 'yaben',
    "F17 Yarawata": 'yarawata',
    "F18 Bilakura": 'bilakura',
    "F19 Parawen": 'parawen',
    "F20 Ukuriguma": 'ukuriguma',
    "F21 Amaimon": 'amaimon',
}



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
                raise ValueError("Bad Line: [*] %s" % filename)
            
            try:
                line = standardise_tabs(line.strip())
            except AssertionError:
                raise ValueError("Tab Standardise Error: %s : %s" % (filename, line))
            
            line = [_.strip() for _ in line.split("\t")]
            for _ in line:
                if ' ' * 3 in _:
                    raise ValueError(u"Dodgy line: %s: %s" % (filename, oline))
            
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
                    raise ValueError(u"Cognate Error: %s - %s" % (filename, e))
            else:
                cogset = None
            
            if len(line):
                raise ValueError("Remainder: '%s' - %s" % ("/".join(line), filename))
            
            if entry:
                for e in entry.split(","):
                    e = clean(e.strip())
                    if len(language) and e:
                        records.append((language, e, sgloss, cogset))
    return records


assert os.path.isdir(DIRNAME), "Cannot find: %s" % DIRNAME


ed = User.objects.get(username="malcolm")

Zgraggen = Source.objects.create(year=1980, author="Z'graggen", slug="zgraggen-1980-nadelbert",
                          reference=REFERENCE, bibtex="", comment="",
                          editor=ed)
                          
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
        wslug = get_wordslug(filename)
        
        try:
            WObj = Word.objects.get(slug=wslug)
        except Word.DoesNotExist:
            print("Unknown WordSlug: %s -- %s" % (wslug, filename))
            raise Word.DoesNotExist("Unknown WordSlug: %s -- %s" % (wslug, filename))
        
        print("Reading File: %s --> %s" % (filename, WObj))
        
        content = readfile(os.path.join(DIRNAME, filename))
        if len(content) < 3:
            raise ValueError("Small file: %s" % filename)
        for l, entry, sgloss, cognates in content:
            LObj = LANGUAGES[l]
            lex = Lexicon.objects.create(
                language=LObj,
                word=WObj,
                source=Zgraggen,
                entry=entry,
                source_gloss=sgloss,
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
