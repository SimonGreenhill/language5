#!/usr/bin/env python
#coding=utf-8

import os
import re
import codecs
from django.contrib.auth.models import User
from website.apps.core.models import Family, Source, Language, AlternateName
from website.apps.lexicon.models import Word, Lexicon, CognateSet, Cognate

DIRNAME = os.path.join(os.environ['IMPORTER_DATAROOT'], '0047_mcelhanon_and_voorhoeve1970')

REFERENCE = "McElhanon, KA & Voorhoeve, CL. 1970. The Trans-New Guinea Phylum: Explorations in deep-level genetic relationships. Canberra: Pacific Linguistics."

IS_BIG_WHITESPACE = re.compile(r"""\s{2,10}""")
IS_LANGUAGE = re.compile(r"""^([\w.]{2,3}\s+[a-z.])""")
IS_LANGUAGE_EXTRA = re.compile(r"""^\.(\w+)""")
IS_COGNATE = re.compile(r"""(\d+)(\w+)?""")

LANGUAGES = {
    "ASK a": 'kamoro',
    "ASK b": 'sempan',
    "ASK c": 'asmat-central',
    
    "AWY a": 'awyu-south',
    "AWY b": 'yenimu',
    "AWY c": 'awyu-asue',
    "AWY d": 'aghu',
    "AWY e": 'mandobo-atas',
    "AWY f": 'wambon',
    
    "OK. a": 'muyu-north',
    "OK. b": 'muyu-south',
    "OK. c": 'ninggerum',
    "OK. d": 'yongkom',
    "OK. e": 'mian',
    "OK. f": 'tifal',
    "OK. g": 'telefol',
    "OK. h": 'faiwol',
    "OK. i": 'bimin',
    "OK. j": 'faiwol',
    
    "APA a": 'aekyom',
    "APA b": 'pare',
    
    "BED a": 'kubo',
    "BED b": 'samo',
    "BED c": 'gobasi-bibo',
    "BED d": 'beami',
    "BED e": 'bosavi',
    
    "FAS .": 'fasu',
    "DUN .": 'duna',
    "MOM .": 'mombum',
    "GOG .": 'gogodala',
    "SUK .": 'suki',
    "MIR .": 'meriam',
    "YEY .": 'yei',
    "MO. .": 'morori',
    "KAN .": 'kanum',
    "KOV .": 'kovai',
    
    "KIW a": 'southern-kiwai',
    "KIW b": 'waboda',
    "KIW c": 'tureture',
    
    "MAR a": 'marind-gawir',
    "MAR b": 'marind-bian',
    
    "BOA a": 'boazi',
    "BOA b": 'kuini',
    "BOA c": 'zimakani-begua',
    
    "YAQ a": 'yaqay',
    "YAQ b": 'kayagar',
    "YAQ c": 'warkay-bipim',
    
    "ORI a": 'gizrra',
    "ORI b": 'bine',
    "ORI c": 'wipi',
    
    "TIR .": 'makayam',
    
    "AGO a": 'agob',
    "AGO b": 'mikud',
    
    "MOR a": 'parb',
    "MOR b": 'keraki',
    "MOR c": 'namo',
    
    "BEN a": 'kunja-peremka',
    "BEN b": 'arammba-setavi',
    
    "YEL a": 'yelmek',
    "YEL b": 'maklew',
    
    "KIM a": 'kimaghima',
    "KIM b": 'ndom',
    "KIM c": 'riantana',
    
    "GOL a": 'korapun-sela',
    "GOL b": 'nalca',
    "GOL c": 'yale-korsarek',
    
    "SEN a": 'sentani',
    "SEN b": 'tanahmerah',
    "SEN c": 'nafri',
    
    "WAR a": 'degenan',
    "WAR b": 'muratayak',
    "WAR c": 'asaroo',
    "WAR d": 'dahating',
    
    "GUS a": 'madi',
    "GUS b": 'ngaing',
    "GUS c": 'neko',
    "GUS d": 'nekgini',
    "GUS e": 'ufim',
    "GUS f": 'iyo',
    "GUS g": 'rawa',
    
    "URU a": 'nukna',
    "URU b": 'nukna-hamelengan',
    "URU c": 'kumdauron',
    "URU d": 'worin',
    "URU e": 'yawan',
    "URU f": 'mitmit',
    "URU g": 'mup',
    "URU h": 'sindamon',
    "URU i": 'kutong-sakam',
    "URU j": 'som',
    
    "YUP a": 'yopno-kewieng',
    "YUP b": 'yopno-nokopo',
    "YUP c": 'domung',
    "YUP d": 'nankina',
    "YUP e": 'bonkiman',

    "WAN a": 'awara',
    "WAN b": 'wantoat-leron',
    "WAN c": 'wantoat',
    "WAN d": 'wantoat-saseng',
    "WAN e": 'wantoat-bam',
    "WAN f": 'wantoat-yagawak',
    "WAN g": 'irumu',

    "ERA a": 'mamaa',
    "ERA b": 'uri',
    "ERA c": 'finongan',
    "ERA d": 'gusan',
    "ERA e": 'nimi',
    "ERA f": 'ma-manda',
    "ERA g": 'numanggang',
    "ERA h": 'nakame',
    "ERA i": 'nek',
    "ERA j": 'nuk',
    "ERA k": 'mungkip',
    
    "WHF a": 'ono-kip',
    "WHF b": 'ono-zankoa',
    "WHF c": 'ono-karako',
    "WHF d": 'sialum',
    "WHF e": 'nomu',
    "WHF f": 'kinalakna',
    "WHF g": 'kumukio',
    "WHF h": 'borong',
    "WHF i": 'burum',
    "WHF j": 'mindik',
    "WHF k": 'tobo',
    "WHF l": 'kube',
    "WHF m": 'timbe',
    "WHF n": 'selepet',
    "WHF o": 'komba',
    "WHF p": 'nabak',
    "WHF q": 'mesem',
    
    "EHF a": 'dedua',
    "EHF b": 'migabac',
    "EHF c": 'momare',
    "EHF d": 'sene',
    "EHF e": 'magobineng',
    "EHF f": 'wamora',
    "EHF g": 'wemo',
    "EHF h": 'mape-naga',
    "EHF i": 'mape-west',
    "EHF j": 'mape-east',
    
    'BIN a': 'suena',
    'BIN b': 'zia',
    'BIN c': 'zia-mawai',
    'BIN d': 'yekora',
    'BIN e': 'binandere',
    'BIN f': 'orokaiva-sairope',
    'BIN g': 'orokaiva-dobuduru',
    'BIN h': 'orokaiva-kendata',
    'BIN i': 'orokaiva-jegarata-kakendetta',
    'BIN j': 'gaina',
    'BIN k': 'ewage-notu',
    'BIN l': 'korafe-yegha',
    'BIN m': 'aeka',
    'BIN n': 'baruga-bareji',
    'BIN o': 'baruga',
    'BIN p': 'binandere-ambasi',
    'BIN q': 'ewage-notu-yega',
    'BIN r': 'orokaiva-waseda',
    'BIN s': 'yega',
    

}
LANGUAGES["Dorro"] = LANGUAGES["MOR c"]
LANGUAGES["Keraki"] = LANGUAGES["MOR b"]
LANGUAGES["Parb"] = LANGUAGES["MOR a"]
LANGUAGES["OK a"] = LANGUAGES["OK. a"]
LANGUAGES["OK b"] = LANGUAGES["OK. b"]
LANGUAGES["OK c"] = LANGUAGES["OK. c"]
LANGUAGES["OK d"] = LANGUAGES["OK. d"]
LANGUAGES["OK e"] = LANGUAGES["OK. e"]
LANGUAGES["OK f"] = LANGUAGES["OK. f"]
LANGUAGES["OK g"] = LANGUAGES["OK. g"]
LANGUAGES["OK h"] = LANGUAGES["OK. h"]
LANGUAGES["OK i"] = LANGUAGES["OK. i"]
LANGUAGES["OK j"] = LANGUAGES["OK. j"]
LANGUAGES["Duna"] = LANGUAGES["DUN ."]


# ERRORS IN THE LIST - these are entries that
# I can't find the definitions for.
DAMN_ERRORS = [
    "SHF", "SHF a", "SHF b", "SHF c", "SHF d",
    "WAN h", "WAN i", "WAN j", "WAN k", "ENa",
    "KIW_Goari", "KIW_Kerewa", "URU k",
    "Kewa", # Don't know which kewa this is.
]

WORDS = {
    '1-arm.txt': 'arm',
    '10-knee.txt': 'knee',
    '11-nail.txt': 'fingernail',
    '12-neck.txt': 'neck',
    '13-skin-bark.txt': 'skin',
    '14-nose.txt': 'nose',
    '15-spittle.txt': 'spittle',
    '16-tongue.txt': 'tongue',
    '17-tooth.txt': 'tooth',
    '18-urine.txt': 'urine',
    '19-name.txt': 'name',
    '2-bone.txt': 'bone',
    '20-elder-brother.txt': 'older-brother',
    '21-elder-sister.txt': 'older-sister',
    '22-mother.txt': 'mother',
    '23-i.txt': 'i',
    '24-we-pl.txt': 'we',
    '25-you.txt': 'you',
    '26-you-pl.txt': 'you-pl',
    '27-he.txt': 'he-she',
    '28-louse.txt': 'louse',
    '29-wing.txt': 'wing',
    '3-breast.txt': 'breast',
    '30-ashes.txt': 'ashes',
    '31-rain.txt': 'rain',
    '32-road.txt': 'road',
    '33-fire.txt': 'fire',
    '34-dog.txt': 'dog',
    '35-leaf.txt': 'leaf',
    '36-noon.txt': 'noontime',
    '37-sand.txt': 'sand',
    '38-smoke.txt': 'smoke',
    '39-star.txt': 'star',
    '4-ear.txt': 'ear',
    '40-sun.txt': 'sun',
    '41-water.txt': 'water',
    '42-wind.txt': 'wind',
    '43-full.txt': 'full',
    '44-long.txt': 'long',
    '45-new.txt': 'new',
    '46-straight.txt': 'straight',
    '47-warm.txt': 'warm',
    '48-burn.txt': 'to-burn',
    '49-eat.txt': 'to-eat',
    '5-eye.txt': 'eye',
    '50-to-shoot.txt': 'to-shoot',
    '51-tie.txt': 'to-tie',
    '52-say-speech-myth-song.txt': 'to-say',
    '53-sleep.txt': 'to-sleep',
    '6-foot-leg.txt': 'leg-foot',
    '7-hair.txt': 'hair',
    '8-head.txt': 'head',
    '999-bird.txt': 'bird',
    '999-man.txt': 'man',
    '999-stone.txt': 'stone',
    '999-woman.txt': 'woman',
    '9a-mouth.txt': 'mouth',
    '9b-lip.txt': 'lips',
}



class Entry(object):
    
    translator = {
        '^': u'ʌ',
        ')': u'ɔ',
        'N': u'ŋ',
        'E': u'ɛ',
        '3': u'ə',
        '?': u'ʔ',
        '~': u'̃',
    }

    def __init__(self, line=None, gloss=None):
        self.line = line
        self.gloss = gloss
        self.language = None
        self.entry = None
        self.cognate = None
        self.annotation = None
        
        if self.line:
            self.parse(self.line)

    def clean(self, s):
        for k,v in self.translator.iteritems():
            s = s.replace(k, v)
        return s
    
    def _check_entry(self, s):
        for a in ascii_letters:
            s = s.replace(a, '')
        for v in self.translator.values():
            s = s.replace(v, '')
        assert len(s) == 0, 'unexpected char in string: %s' % s
    
    def _check_language(self, s):
        s = [_.strip() for _ in s.split(" ") if len(_.strip()) > 0]
        if s[0][-1] == '.':
            s[0] = s[0].replace('.', '')
        return " ".join(s)
    
    def parse(self, entry):
        entry = entry.strip()
        # annot
        if '//' in entry:
            entry, self.annotation = [e.strip() for e in entry.split("//")]
            self.annotation = self.clean(self.annotation)
        
        if IS_LANGUAGE.match(entry):
            self.language = self._check_language(IS_LANGUAGE.findall(entry)[0])
            entry = IS_LANGUAGE.sub("", entry, 1).strip()
        elif IS_LANGUAGE_EXTRA.match(entry):
            self.language = self._check_language(IS_LANGUAGE_EXTRA.findall(entry)[0])
            entry = IS_LANGUAGE_EXTRA.sub("", entry, 1).strip()
        else:
            raise ValueError("Unable to find Language in %s" % self.line)
        
        # cog
        try:
            entry, cog = IS_BIG_WHITESPACE.split(entry)
            self.cognate = self._check_cognate(cog)
        except ValueError:
            cog = None
        
        # gloss
        if '|' in entry:
            entry, self.gloss = entry.split("|")
        self.entry = self.clean(entry)
         
        #try:
        #    self._check_entry(self.entry)
        #except AssertionError:
        #    print("Error on %s" % self.entry)
        #    #raise

    def _check_cognate(self, obj):
        return obj
    
    def __repr__(self):
        if self.annotation:
            template = u"%(language)s: %(gloss)s: %(entry)s (%(annotation)s) |%(cognate)s"
        else:
            template = u"%(language)s: %(gloss)s: %(entry)s |%(cognate)s"
        template = unicode(template) % { 
            'language': self.language,
            'gloss': self.gloss,
            'cognate': self.cognate,
            'entry': self.entry,
            'annotation': self.annotation,
        }
        return template


def read_file(filename, gloss):
    entries = []
    with codecs.open(filename, 'rU', encoding="utf-8") as handle:
        for line in handle.readlines():
            line = line.strip()
            if len(line) == 0:
                continue
            elif line.startswith("#"):
                continue
            else:
                e = Entry(line, gloss=gloss)
                if e.entry:
                    entries.append(e)
    return entries


def get_cognate_sets(cognate):
    if cognate is None:
        return None
    cognates = []
    for c in IS_COGNATE.findall(cognate):
        if c[1] == u'' or c[1] == 'x':
            cognates.append(c[0])
        else:
            cognates.append(c[0])
            cognates.append("".join(c))
    return list(set(cognates))
    

assert os.path.isdir(DIRNAME), "Cannot find: %s" % DIRNAME

ed = User.objects.get(username="simon")

SObj = Source.objects.create(
        year=1970, 
        author="McElhanon and Voorhoeve", 
        slug="mcelhanon_and_voorhoeve1970",
        reference=REFERENCE, 
        bibtex="", 
        comment="",
        editor=ed)
                          

lex_counter = 0
cognate_sets = {} # key = (filename, number)
for filename in os.listdir(DIRNAME):
    entries = read_file(os.path.join(DIRNAME, filename), gloss=WORDS[filename])
    
    print filename.ljust(20), '->'
    
    for e in entries:
        errors = []
        
        if e.language in DAMN_ERRORS:
            continue
        
        try:
            WObj = Word.objects.get(slug=e.gloss)
        except Word.DoesNotExist:
            raise Word.DoesNotExist("Unknown WordSlug: %s -- %s" % (e.gloss, filename))
            
        
        try:
            LObj = Language.objects.get(slug=LANGUAGES[e.language])
        except Language.DoesNotExist:
            raise Language.DoesNotExist("Unknown Language: %s -> %s" % (e.language, LANGUAGES[e.language]))
        except KeyError:
            raise Language.DoesNotExist("Undefined Language: %s" % e.language)
            
        ann = e.annotation if e.annotation is not None else ''
        print "\t", '%5d' % lex_counter, e.language, '=', LObj.slug.ljust(20), WObj.slug.ljust(15), e.entry.ljust(10), e.cognate, ann
        lex = Lexicon.objects.create(
                         language=LObj,
                         word=WObj,
                         source=SObj,
                         entry=e.entry,
                         source_gloss=e.gloss,
                         annotation=e.annotation,
                         editor=ed
        )
        lex_counter += 1
        
        if e.cognate is not None:
            for c in get_cognate_sets(e.cognate):
                cogid = (c, filename)
                cognate_sets[cogid] = cognate_sets.get(cogid, [])
                cognate_sets[cogid].append(lex)
    

# # Handle cognates
cog_counter, cset_counter = 0, 0
for key in cognate_sets:
    cogid, filename = key
    WObj = Word.objects.get(slug=WORDS[filename])
    
    CogSet = CognateSet.objects.create(
        protoform='',
        gloss=WObj.word,
        source=SObj,
        comment="McElhanon and Voorhoeve 1970: %s-%s" % (WORDS[filename], cogid),
        quality='1', # published
        editor=ed
    )
    CogSet.save()
    cset_counter += 1
    print("Created CognateSet obj %d: %s" % (CogSet.id, CogSet.comment))
    
    for m in cognate_sets[key]:
        cog = Cognate.objects.create(lexicon=m, cognateset=CogSet, source=SObj, editor=ed)
        cog.save()
        cog_counter += 1
        print(" %5d: %s << %s" % (cog_counter, CogSet, m))


print("\n\n")
print("========================================")
print("Created %d Lexical Items" % lex_counter)
print("Created %d Cognate Sets" % cset_counter)
print("Created %d Cognates" % cog_counter)
