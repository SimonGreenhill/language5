#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import codecs

import locale
locale.setlocale(locale.LC_ALL, "")
#print locale.getlocale()

from django.contrib.auth.models import User
from website.apps.core.models import Language, Source, AlternateName, Family
from website.apps.lexicon.models import Lexicon, Word, CognateSet, Cognate

ed = User.objects.get(pk=1) # get editor


REFERENCE = """Dutton, T.E., 2010. Reconstructing Proto Koiarian: The history of a Papuan language family, Canberra: Pacific Linguistics."""

BIBTEX = """@book{Dutton2010,
address = {Canberra},
author = {Dutton, T. E.},
isbn = {9780858836099},
publisher = {Pacific Linguistics},
title = {Reconstructing Proto Koiarian: The history of a Papuan language family},
year = {2010}
}
"""


PROTOLANGUAGE = {
    'd.dat': 'Proto-Koiarian',
    'e.dat': 'Proto-Koiaric',
    'f.dat': 'Proto-Baraic',
}

LANGUAGES = {
    'Proto-Koiarian': Language.objects.create(editor=ed,
        language = "Proto-Koiarian",
        slug = "proto-koiarian",
        isocode = "",
        classification = "Trans-New Guinea, Southeast Papuan, Koiarian"
    ),
    'Proto-Koiaric': Language.objects.create(editor=ed,
            language = "Proto-Koiariac",
            slug = "proto-koiraric",
            isocode = "",
            classification = "Trans-New Guinea, Southeast Papuan, Koiarian, Koiaric"
    ),
    'Proto-Baraic': Language.objects.create(editor=ed,
                language = "Proto-Baraic",
                slug = "proto-baraic",
                isocode = "",
                classification = "Trans-New Guinea, Southeast Papuan, Koiarian, Baraic"
    ),
    
    'Koitabu': Language.objects.create(editor=ed,
                language = "Koitabu",
                slug = "koitabu",
                isocode = "kqi",
                classification = "Trans-New Guinea, Southeast Papuan, Koiarian, Koiaric"
    ),
    'Koiari': Language.objects.create(editor=ed,
                language = "Grass Koiari",
                slug = "grass-koiari",
                isocode = "kbk",
                classification = "Trans-New Guinea, Southeast Papuan, Koiarian, Koiaric"
    ),
    'Mountain Koiari': Language.objects.create(editor=ed,
                language = "Mountain Koiari",
                slug = "mountain-koiari",
                isocode = "kpx",
                classification = "Trans-New Guinea, Southeast Papuan, Koiarian, Koiaric"
    ),
    
    
    'Managalasi': Language.objects.create(editor=ed,
                language = "Ese",
                slug = "ese",
                isocode = "mcq",
                classification = "Trans-New Guinea, Southeast Papuan, Koiarian, Baraic"
    ),
    
    
    'North Barai': Language.objects.create(editor=ed,
                language = "Barai",
                dialect = "North",
                slug = "north-barai",
                isocode = "bbb",
                classification = "Trans-New Guinea, Southeast Papuan, Koiarian, Baraic"
    ),
    'South Barai': Language.objects.create(editor=ed,
                language = "Barai",
                dialect = "South",
                slug = "south-barai",
                isocode = "bbb",
                classification = "Trans-New Guinea, Southeast Papuan, Koiarian, Baraic"
    ),
    u'Ömie': Language.objects.create(editor=ed,
                language = u'Ömie',
                slug = "omie",
                isocode = "aom",
                classification = "Trans-New Guinea, Southeast Papuan, Koiarian, Baraic"
    ),
}

WORD_OVERRIDES = {
    'get, take': 'to-get',
    #'man, husband': ('man') # ADD THIS ONE. 
    'push': 'to-push',
    'person, human being': 'person',
    'see': 'to-see',
    'bite': 'to-bite',
    'sleep, lie down': 'to-lie',
    'sleep': 'to-sleep',
    'dig (hole)': 'to-dig',
    'tie, fasten': 'to-tie',
    'sew up': 'to-sew',
    'go': 'to-go',
    'swim': 'to-swim',
    'fight': 'to-fight',
    'think': 'to-think',
    'woman, wife': 'woman',
    'father (reference)': 'father',
    'father (address)': 'father',
    'sit down': 'to-sit',
    'sit': 'to-sit',
    'laugh': 'to-laugh',
    'mosquito, gnat': 'mosquito',
    'die': 'to-die',
    'and (joining NPs)': 'and',
    'pull': 'to-pull',
    'vomit': 'to-vomit',
    'wind (breeze)': 'wind',
    'scratch (skin)': 'to-scratch',
    'wash (stg)': 'to-wash',
    'wash': 'to-wash',
    'come': 'to-come',
    'say, speak, talk': 'to-say',
    'dance, sing': 'to-dance',
    'to blow (fire)': 'to-blow',
    'hit': 'to-hit', 
    'and (joining nouns)': 'and',
    'afterwards, later': 'afterwards',
    'cry, weep': 'to-cry',
    'burn (vi)': 'to-burn',
    'hole (in ground)': 'hole',
    'cook (on hot stones)': 'to-cook',
    '(a)rise, get up, stand up (from sitting)': 'to-stand',
    'not, negative': 'not',
    'give (sg. IO)': 'to-give',
    'stone, rock': 'stone',
    'fall down': 'to-fall',
    'hot': 'warm',
    'string, rope': 'rope',
    'talk, speak': 'to-talk',
    'rotten, rotting': 'rotten',
    'ground, earth': 'ground',
    'cut, cut off, slice': 'to-cut',
    'wash (sg obj)': 'to-wash',
    'wash oneself, bathe': 'to-wash',
    'stand (sg. subject)': 'to-stand',
    'vine, string, rope': 'rope',
    'path, road': 'road',
    'milk, juice': 'milk',
    'plant (garden)': 'to-plant',
    'egg, kernel': 'egg',
    'stop, leave off': 'to-stop',
    'stay, be in a place, live': 'to-stay',
    'nape of neck': 'neck',
    'long ago, before, old': 'before',
    'middle, tongue': 'tongue',
    'stomach, intestines, faeces': 'belly',
    'cut, chop (wood)': 'to-cut',
    'tree, stick, pole, log': 'tree',
    'hear, understand, feel': 'to-hear',
    'land, ground, place': 'ground',
    'burn, cook (by burning)': 'to-burn',
    'new, uncooked, raw, young': 'new',
    'animal, game, meat': 'animal',
    'he, she, it': 'he'
}



EXPECTED_CREATES = [
    'man, husband', 'son', 'urinate', 'pawpaw', 'bed bug', 'lizard', 'penis',
    'how much?', 'garden', 'bush', 'navel', 'vagina', 'spear (N)', 'ripe', 
    'which?', 'to spear', 'anus, buttocks', 'to run', 'top', 'pour out', 'now',
    'only', 'also', 'quickly', 'cooked', '(honey) bee', 'yam', 'to cough', 'Relative',
    'to be afraid', 'purposive verb suffix', 'predicative possessive suffix',
    'locative noun suffix', 'PL suffix on kinship nouns',
    "Locative noun suffix (at, to, from)", "medial SS verb suffix",
    'work (n)', 'interrogative particle (generally suffixed to subject)',
    'to chew', "or", 'to call out', 'leech', 'taro', 'body', 'forehead, face', 
    'you (sg)', 'you (pl)', 'medial verb suffix DS', 'thigh', 
    'having finished that, and then (Medial Sequential Suffix)',
    'to sneeze', 'side', 'old woman', 'boy, male child', 
    'OR PL in some verbs', "verb suffix, past tense SG", "Medial Verb Suffix",
    'OR SG in some verbs', 'no, not', 'Predictive possessive suffix', 
    'to open', "Cordyline sp.", 'trunk (of tree)', 'breadfruit',
    'verb suffix, present continuous, SG', "yesterday, tomorrow",
    "day before yesterday, day after tomorrow", 'to ascend',
    'jaw, chin', 'to pain', 'to chop, cut down', 'to drill',
    '(immediate) imperative plural verb suffix', 'fire, firewood',
    'sibling, same sex, younger', 'sibling, same sex, older',
    "for, benefactive (cliticised or suffixed to noun)", 
    'transitive verb forming suffix, causative', 'hair, fur, feathers',
    'to return', 'to scrape off', 'break wood', 'to enter', 'sun, day',
    'a (certain one), some, another', 'to do, make', 'to spin, twirl', 
    'to perspire, sweat', 'raised land, ridge', 'sibling, opposite sex, older',
    'to buy, sell, barter', 'to eat, drink', 'noose, trap, net',
    'like, similar', 'cook (in ground on hot stones), mumu', 
    'back (of hand), top (of foot)', 'to break', "plateau, flat land",
    'with (by means of)', 'to clear bush for planting', 'cloth, clothes',
    'if, when (conditional verb suffix)', 'to dig up', 'to joke',


]

class Record(object):
    
    _languages = {
        'kta': 'Koitabu',
        'koi': 'Koiari',
        'man': 'Managalasi',
        'bar(n)': 'North Barai',
        'bar(s)': 'South Barai',
        'mtn': 'Mountain Koiari',
        'omi': u'Ömie',
    }
    
    def __init__(self, record):
        self.language = None
        self.language_token = None
        self.entry = None
        self.gloss = None
        self.comment = None
        
        self.process(record)
        
    def __repr__(self):
        o = "%s /%s/ \"%s\" : %s" % (self.language, self.entry, self.gloss, self.comment)
        return unicode(o)#.encode('utf-8')

    def get_language(self, token):
        if token not in self._languages:
            raise ValueError("Unknown Language: %s" % token)
        return self._languages[token]


    def process(self, record):
        record = [x.strip() for x in record.split(" : ")]
        # language
        self.language_token = record[0]
        self.language = self.get_language(self.language_token)
        # entry
        try:
            self.entry = record[1]
        except IndexError:
            pass
        
        # gloss
        try:
            self.gloss = record[2].lstrip("'").strip("'")
        except IndexError:
            pass
        
        # comment
        try:
            self.comment = record[3]
        except IndexError:
            pass



class Entry(object):
    def __init__(self, chunk):
        # init.
        self.pid = None
        self.protoform = None
        self.gloss = None
        self.comment = None
        self.comment2 = None
        self.records = []
        # process 
        self.process(chunk)
    
    def get_comment(self):
        if self.comment2 is None:
            return self.comment
        else:
            return "%s\n%s" % (self.comment, self.comment2)
        
        
    def split(self, line):
        "Splits a line, returning a tuple of (token, remainder)"
        p = line.find(":")
        if p == -1:
            raise ValueError("Invalid Line Format: %s" % line)
        token = line[0:p].strip()
        remainder = line[p+1:].strip()
        if len(remainder) == 0:
            remainder = None
        return (token, remainder)

    def process(self, chunk):
        for line in chunk.split("\n"):
            line = line.strip()
            if len(line) == 0:
                continue
            token, remainder = self.split(line)
            
            if token == 'RECORD':
                self.records.append(Record(remainder))
            elif token == 'PROTOFORM':
                self.pid, self.protoform = [x.strip() for x in
                                            remainder.split(".", 1)]
            elif token == 'PROTOFORM GLOSS':
                self.gloss = remainder
            elif token == 'PROTOFORM COMMENT':
                self.comment = remainder
            elif token == 'COMMENT':
                self.comment2 = remainder
            else:
                raise ValueError("Unhandled state: %s" % line)
        
    def dump(self):
        for attr in ('pid', 'protoform', 'gloss', 'comment', 'comment2'):
            print attr.ljust(20), "\t", getattr(self, attr, None)
        print
        for r in self.records:
            print '->', r


def read(filename):
    chunks = []
    chunk = []
    with codecs.open(filename, 'rU', encoding="utf8") as handle:
        for line in handle.readlines():
            line = line.strip()
            if line.startswith("-") and line.endswith("-"):
                if len(chunk) > 0:
                    chunks.append("\n".join(chunk))
                    chunk = []
            else:
                chunk.append(line)
    if len(chunk) > 0:
        chunks.append("\n".join(chunk))
    return chunks




for langobj in LANGUAGES.values():
    print 'Created Language:', langobj
    langobj.save()
    
# add some altnames
a = AlternateName.objects.create(editor=ed, 
    language=LANGUAGES['Koitabu'], name="Koita", slug="koita"
)
print 'Created AltName:', a
a = AlternateName.objects.create(editor=ed, 
    language=LANGUAGES['Managalasi'], name="Managalasi", slug="managalasi"
)
print 'Created AltName:', a

# add families
family = Family.objects.get(slug="transnewguinea")
for langobj in LANGUAGES.values():
    langobj.family.add(family)


source = Source.objects.create(editor=ed,
    year=2010, author="Dutton", slug="dutton2010",
    reference=REFERENCE, bibtex=BIBTEX, comment=""
)
source.save()
print 'Created Source:', source

counter_lex = 0
counter_pfm = 0
counter_cog = 0
counter_wrd, counter_fwd = 0, 0

for filename, p in PROTOLANGUAGE.items():
    assert p in LANGUAGES
    protolanguage = LANGUAGES[p]
    entries = read(os.path.join(os.environ["IMPORTER_DATAROOT"], '0006_dutton2010', filename))
    for e in sorted(entries):
        e = Entry(e)
        ###e.dump()
        if e.gloss in WORD_OVERRIDES:
            wslug = WORD_OVERRIDES[e.gloss]
        else:
            wslug = e.gloss.replace(' ', '-').replace("?", "").lower()
            wslug = wslug.replace("(", "").replace(")", "").replace(",", "")
            wslug = wslug.replace('"', '').replace("'", '')
        # 1  get_or_create word
        try:
            word = Word.objects.get(slug=wslug)
            counter_fwd += 1
            print 'Found Word:', counter_fwd, word
        except:
            assert e.gloss in EXPECTED_CREATES, 'Expected %s/%s in EXPECTED_CREATES' % (e.gloss, wslug)
            word = Word.objects.create(slug=wslug, word=e.gloss, editor=ed)
            counter_wrd += 1
            print 'Created Word:', counter_wrd, word
            
        # 2. add protoform
        pform = CognateSet.objects.create(
            editor=ed,
            protoform=e.protoform,
            gloss=e.gloss,
            comment=e.get_comment(),
            source=source,
            quality="1" # published
        )
        pform.save()
        counter_pfm += 1
        print 'Created Protoform:', counter_pfm, pform
        
        # add protoform to proto-language
        lex = Lexicon.objects.create(
            editor=ed,
            language=protolanguage,
            source=source,
            word=word,
            entry=e.protoform,
            annotation=''
        )
        lex.save()
        counter_lex += 1
        print 'Created Lexicon: ', counter_lex, lex
        
        for rec in e.records:
            
            lang = LANGUAGES[rec.language]
            
            if rec.entry == ':' or rec.entry == '::' or rec.entry == ': :':
                pass #continue
            else:
                for entry in rec.entry.split(","):
                    entry = entry.strip()
                        
                    lex = Lexicon.objects.create(
                        editor=ed,
                        language=lang,
                        source=source,
                        word=word,
                        entry=entry,
                        annotation=rec.gloss
                    )
                    lex.save()
                    counter_lex += 1
                    print 'Created Lexicon: ', counter_lex, lex, repr(lex.annotation)
                    # cognate
                    cog = Cognate.objects.create(
                        editor=ed,
                        cognateset=pform,
                        source=source,
                        lexicon=lex,
                        comment=rec.comment,
                        flag='1' # published
                    )
                    cog.save()
                    counter_cog += 1
                    print 'Create Cognate: ', counter_cog, cog
                

print '='*76
print 'TOTAL PROTOFORMS', counter_pfm
print 'TOTAL WORDS FOUND', counter_fwd
print 'TOTAL WORDS CREATED', counter_wrd
print 'TOTAL LEXICON', counter_lex
print 'TOTAL COGNATES', counter_cog
                