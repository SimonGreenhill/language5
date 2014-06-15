#!/usr/bin/env python
#coding=utf-8

import os
import re
import codecs
from django.contrib.auth.models import User
from website.apps.core.models import Family, Source, Language, AlternateName
from website.apps.lexicon.models import Word, Lexicon, CognateSet, Cognate

from synonyms import SYNONYMS, find_synonym

DIRNAME = os.path.join(os.environ['IMPORTER_DATAROOT'], '0043_zgraggen_mabuso')
REFERENCE = "Z'graggen, J.A., 1980. A comparative word list of the Mabuso Languages, Madang Province, Papua New Guinea, Canberra: Pacific Linguistics."

IS_DIGIT = re.compile(r"\d\d+")

# Specific synonyms for this dataset
SYNONYMS.update({
    'lightening': 'lightning',
    'flyv': 'to-fly',
    'flyn': 'fly-sp',
    'NegationMarker': 'negation-marker',
    'PossessiveMarker': 'possessive-marker',
    'male-of-animals': 'male',
    'female-of-animals': 'female',
    'inside': 'in',
    'spear': 'spear-n',
    'spear-fish-spear': 'fish-spear',
    'calf-of-leg': 'calf',
    'to-chop-cut-down': 'to-chop',
    'I-1st-person-singular': 'i',
    'thou-free-D:2S': 'you',
    'he-free-D:3S-': 'he-she',
    'he-free-D:3S': 'he-she',
    'we-two-free': 'we-dual',
    'we-free-D:1P': 'we',
    'you-two-free': 'you-dual',
    'ye-free-D:2P': 'you-pl',
    'they-two-free': 'they-dual',
    'they-free-D:3P': 'they',
    'fight-hit': 'to-fight',
    'tie': 'to-tie',
    'fasten': 'to-fasten',
    'potato': 'sweet-potato',
    'stone-axe': 'axe',
    'axe-iron': 'axe-iron',
    
    # VO / o
    'O:1S-VerbalObject': 'me',
    'thou-VO-O:2S': 'you-o2s',
    'he-VO-O:3S': 'him-her-it',
    'we-VO-O:1P': 'us',
    'we-two-vo': 'us-two',
    'you-two-vo': 'you-pl-dual-o2p',
    'ye-VO': 'you-pl-o2p',
    'they-two-vo': 'them-dual',
    'they-VO-O:3P': 'them',
       
     # P
     'I-gen-P:1S': 'my',
     'thou-genitive-P:2S': 'your-sg',
     'he-gen-P:3S': 'his',
    
     'we-gen': 'our',
     'we-two-gen': 'our-dual',
    
     'ye-gen': 'your-pl',
     'you-two-gen': 'your-pl-dual',
    
     'they-two-gen': 'their-dual',
     'they-gen-P:3P': 'their',
     
        
})

LANGUAGES = {
    'C1 Kare': 'kare',
    'C2 Girawa': 'girawa',
    'C3 Munit': 'munit',
    'C4 Bemal': 'kein',
    'C5 Sihan': 'sihan',
    'C6 Gumalu': 'gumalu',
    'C7 Isebe': 'isebe',
    'C8 Amele': 'amele',
    'C9 Bau': 'bau',
    'C10 Panim': 'panim',
    'C11 Rapting': 'rapting',
    'C12 Wamas': 'wamas',
    'C13 Samosa': 'samosa',
    'C14 Murupi': 'murupi',
    'C15 Saruga': 'saruga',
    'C16 Nake': 'nake',
    'C17 Mosimo': 'mosimo',
    'C18 Garus': 'garus',
    'C19 Yoidik': 'yoidik',
    'C20 Rempi': 'rempi',
    'C21 Bagupi': 'bagupi',
    'C22 Silopi': 'silopi',
    'C23 Utu': 'utu',
    'C24 Mawan': 'mawan',
    'C25 Baimak': 'baimak',
    'C26 Matepi': 'matepi',
    'C27 Gal': 'gal',
    'C28 Garuh': 'nobonob',
    'C29 Kamba': 'wagi',
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


def process_cognate(cog):
    if '?' in cog:
        return None
    try:
        return int(cog)
    except:
        raise ValueError(u"Cogset Error: %s" % cog)
    return None


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

Zgraggen = Source.objects.create(year=1980, author="Z'graggen", slug="zgraggen-1980-mabuso",
                          reference=REFERENCE, bibtex="", comment="",
                          editor=ed)
                          
Ross2014 = Source.objects.get(slug="Ross2014")

# check languages
l2 = {}
for l in LANGUAGES:
    l2[l] = Language.objects.get(slug=LANGUAGES[l])
LANGUAGES = l2

cognates = {}
lex_counter = 0
for filename in get_filenames(DIRNAME):
    if filename.endswith('.txt'):
        wslug = get_wordslug(filename)
        
        try:
            WObj = Word.objects.get(slug=wslug)
        except Word.DoesNotExist:
            raise Word.DoesNotExist("Unknown WordSlug: %s -- %s" % (wslug, filename))
        
        print("Reading File: %s --> %s" % (filename, WObj))
        
        content = readfile(os.path.join(DIRNAME, filename))
        for l, entry, sgloss, cognate in content:
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
            print(" %5d created %4d. %20s - %20s %s" % (lex_counter, lex.id, lex.entry, lex.source_gloss, cognate))
            
            if cognate is not None:
                key = (cognate, WObj)
                cognates[key] = cognates.get(key, [])
                cognates[key].append(lex)


# Handle cognates
cog_counter = 0
for key in cognates:
    cogid, WObj = key
    # TODO: get_or_create lookup cognate with MDR <XX>
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
        print("Created CognateSet obj %d: %s" % (CogSet.id, CogSet.comment))
        
    for m in cognates[key]:
        cog = Cognate.objects.create(lexicon=m, cognateset=CogSet, source=Ross2014, editor=ed)
        cog.save()
        cog_counter += 1
        print(" %5d: %s << %s" % (cog_counter, CogSet, m))
        