#!/usr/bin/env python
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# import models
from website.apps.core.models import Source, Language
from website.apps.lexicon.models import Lexicon, Word, CognateSet, Cognate

# importer sets some variables
import os
import re
import xlrd
from collections import Counter

FILES = [
    os.path.join(os.environ['IMPORTER_DATAROOT'], '0009_binandere', 'cognate sets a-l.xls'),
    os.path.join(os.environ['IMPORTER_DATAROOT'], '0009_binandere', 'cognate sets m-z.xls'),
]

LANGUAGE_LIST = {
    '00G-S': 'Guhu-Samane',
    '00Tah': 'Tahari',
    '01Y-Y': 'Yema-Yarawe',
    '01Sue': 'Suena',
    '02Yek': 'Yekora',
    '03Zia': 'Zia',
    '04Maw': 'Mawae',
    '05Bin': 'Binandere',
    '06Amb': 'Ambasi',
    '07Aek': 'Aeka',
    
    '08Oro': 'Orokaiva', 
    '08Sos': 'Sose',
    '08J-S': 'Jegasa-Sarau',
    '08Dob': 'Dobuduru',
    '08J-K': 'Jegarata-Kakendetta',
    '08Ken': 'Kendata', 
    '08Par': 'Para Harava',
    
    '09Hun': 'Hunjara',
    '09Kok': 'Kokoda',
    '09Sai': 'Sairope',
    
    '10Not': 'Notu',
    
    '11Yeg': 'Yega', 
    '11A-D': 'Ambe-Dofo',
    '11Ouk': 'Oukena', 
    
    '12Gae': 'Gaena',
    '12Brj': 'Bareji',
    '12Gen': 'Gena',
    '12Kar': 'Karoto',

    '13Bar': 'Baruga',
    '13TBa': 'Tafota Baruga',
    '13MBa': 'Mado Baruga',
    '13BBa': 'Bareji Baruga',

    '14Dog': 'Doghoro',
    '15Kor': 'Korafe',
    '15Mok': 'Mokorua',
    '15Rab': 'Rabade',
}


PROTOLANGUAGE_TOKENS = {
    'pBin': re.compile(r'\bpBin\b'), 
    'CstBin': re.compile(r'\bCstBin\b'), 
    'NucBin': re.compile(r'\bNucBin\b'), 
    'SthBin': re.compile(r'\bpSthBin\b'),
    'pNthBin': re.compile(r'\bpNthBin'),
    
    'xOro': re.compile(r'\bOro dialects only'),
    'xBar': re.compile(r'\bBar dialects only\b'),
}

LANGUAGE_SLUGS = {
    'pBin': 'proto-binandere',    
    'cstBin': 'proto-coastal-binandere',
    'CstBin': 'proto-coastal-binandere',
    'NucBin': 'proto-nuclear-binandere',
    'SthBin': 'proto-south-binandere',
    'pNthBin': 'proto-north-binandere',
    'xOro': 'proto-orokaiva',
    'xBar': 'proto-baruga',
    
    'Rabade': 'rabade',
    'Mokorua': 'mokorua',
    'Tafota Baruga': 'baruga-tafota',
    'Mado Baruga' :  'baruga-mado',
    'Bareji Baruga': 'baruga-bareji',
    'Bareji': 'bareji',
    'Karoto': 'karoto',
    'Gena': 'gena',
    'Oukena': 'oukena',
    'Ambe-Dofo': 'ambe-dofo',
    'Jegasa-Sarau': 'orokaiva-jegasa-sarau',
    'Sose': 'orokaiva-sose',
    'Para Harava': 'orokaiva-para-harava',
    'Kokoda': 'hunjara-kaina-ke-kokoda',
    'Sairope': 'orokaiva-sairope',
    'Kendata': 'orokaiva-kendata',
    'Jegarata-Kakendetta': 'orokaiva-jegarata-kakendetta',
    'Guhu-Samane': 'guhu-samane',
    'Tahari': 'guhu-samane-tahari',
    'Yema-Yarawe': 'suena-yema-yarawe',
    'Suena': 'suena',
    'Yekora': 'yekora',
    'Zia': 'zia',
    'Mawae': 'zia-mawai',
    'Binandere': 'binandere',
    'Ambasi': 'binandere-ambasi',
    'Aeka': 'aeka',
    'Orokaiva': 'orokaiva',
    'Dobuduru': 'orokaiva-dobuduru',
    'Hunjara': 'hunjara-kaina-ke',
    'Notu': 'ewage-notu',
    'Yega': 'yega',
    'Gaena': 'gaina',
    'Baruga': 'baruga',
    'Doghoro': 'doghoro',
    'Korafe': 'korafe',
}

SOURCE_SLUG = "smallhorn-2011"


# simple logger
class Logger(object):
    def __init__(self):
        self.counter = {'cognates': 0, 'words': 0, 'cognatesets': 0, 'lexicon': 0, 'languages': 0}
        
    def echo(self, obj, created=False):
        if isinstance(obj, Word):
            if created: self.counter['words'] += 1
            _type = 'Word'
        elif isinstance(obj, CognateSet):
            if created: self.counter['cognatesets'] += 1
            _type = 'CognateSet'
        elif isinstance(obj, Cognate):
            if created: self.counter['cognates'] += 1
            _type = 'Cognate'
        elif isinstance(obj, Lexicon):
            if created: self.counter['lexicon'] += 1
            _type = 'Lexicon'
        elif isinstance(obj, Language):
            if created: self.counter['languages'] += 1
            _type = 'Language'
        else:
            raise ValueError("%r" % obj)
        
        token = '+' if created else ' '
        print("\t {} {}: {}".format(token, _type, obj))
        
    def dump(self):
        for k, v in self.counter.items():
            print("{} \t\t\t = {}".format(k, v))
        

def guess_protolanguage(notes):
    "Guesses which protolanguage is being reconstructed"
    for n in notes:
        for plang, pmatch in PROTOLANGUAGE_TOKENS.items():
            if pmatch.findall(n):
                return plang
            elif n == '?':
                return None # No protolanguage
    raise ValueError("Unable to find proto-language in %r" % notes)


re_headline = re.compile(r'(\d+)\.\s+(.*)(\*.*)')
def process_headline(headline):
    "Process the headline"
    try:
        h = re_headline.findall(headline)[0]
    except:
        raise ValueError("Unable to process headline %s" % headline)
    
    assert len(h) == 3, "expected 3 chunks for headline %s" % headline
    assert int(h[0]), "%r is not an integer in headline %s" % (h[0], headline)
    assert h[2].startswith("*"), "%r doesn't look like a reconstruction in %s"\
        % (h[2], headline)
    
    h = [_.strip() for _ in h]
    return h

def get_content(sheet):
    "Loads content from the given sheet."
    # get headline
    headline = None
    row = sheet.row(0)
    assert len(row[0].value) > 0
    # check everything else in this row is empty.
    for cell in row[1:]:
        assert cell.value == u''
    headline = row[0].value    
    
    # process header
    header = [c.value for c in sheet.row(1)]
    assert header[0] == u'Language'
    assert header[1] == u'Lexeme'
    
    # process content
    languages = []
    notes = []
    in_notes = False # flag for parsing notes section
    for i in range(2, sheet.nrows):
        row = sheet.row(i)
        
        # set flag if we're in notes section
        if row[0].value == u'Notes':
            in_notes = True
        
        # ignore empty rows
        if len(u"".join([unicode(c.value) for c in row])) == 0:
            continue
        
        # ignore unwanted.
        if row[0].value.upper() == u'DO NOT INCLUDE THIS SET.':
            return (None, None, None)
        if row[0].value.upper() == u'THIS SET EXCLUDED.':
            return (None, None, None)

        # In notes section, add to notes list.
        if in_notes:
            note = row[0].value.strip()
            if note == u'Notes':
                pass
            else:
                notes.append(note)

        # Not in notes section, process real data
        else:
            row = dict(zip(header, [c.value for c in row]))
            # get real language name
            row['Language'] = LANGUAGE_LIST[row['Language']]
            
            languages.append(row)
   
    assert len(languages) > 0
    return (headline, languages, notes)


def add_lexicon(language, source, word, entry, editor, annotation=""):
    lex = Lexicon.objects.create(
        language=language, 
        source=source,
        word=word, 
        entry=entry, 
        annotation=annotation, 
        editor=editor
    )
    lex.save()
    return lex
    


ed = User.objects.get(pk=1)   # get editor
SObj = Source.objects.get(slug="smallhorn-2011")  # get source

logger = Logger()

for xlname in FILES:
    assert os.path.isfile(xlname), "Unable to find %s" % xlname
    xl = xlrd.open_workbook(xlname)
    
    for sheet in xl.sheets():
        try:
            headline, languages, notes = get_content(sheet)
        except Exception as e:
            print "Unable to read sheet %s" % sheet.name
            raise
            
        if headline is None:
            continue
        
        hid, english, reconstr = process_headline(headline)
        
        print '#', hid, english, reconstr
        
        # Guess word
        wslug = slugify(english)
        try:
            WObj = Word.objects.get(slug=wslug)
            logger.echo(WObj, False)
        except Word.DoesNotExist:
            WObj = Word.objects.create(word=english, slug=wslug, editor=ed)
            WObj.save()
            logger.echo(WObj, True)
            
        
        # create a cognate set
        CogSet = CognateSet.objects.create(
            protoform=reconstr,
            gloss=english,
            source=SObj,
            comment="\n".join(notes),
            quality='1', # published
            editor=ed
        )
        CogSet.save()
        logger.echo(CogSet, True)
        
        # find protolanguage
        protolanguage = guess_protolanguage(notes)
        protoslug = LANGUAGE_SLUGS.get(protolanguage)
        
        if protolanguage is not None:
            LObj = Language.objects.get(slug=protoslug)
            logger.echo(LObj, False)
            
            # Add as lexicon for this protolanguage. 
            lex = add_lexicon(LObj, SObj, WObj, reconstr, ed)
            logger.echo(lex, True)
        
            # and as a cognate...
            cog = Cognate.objects.create(lexicon=lex, cognateset=CogSet, source=SObj, editor=ed)
            cog.save()
            logger.echo(cog, True)

        
        
        # loop through items
        for l in languages:
            #{u'Language': 'Baruga', u'PoS': u'n', u'Lexeme': u'di\u0263i', 
            # u'Source': u'TD68', u'English Gloss': u'louse', u'Ref': u'22'}        
            langslug = LANGUAGE_SLUGS.get(l['Language'])
            assert langslug is not None and len(langslug)
            LObj = Language.objects.get(slug=langslug)
            
            # Add as lexicon
            lex = add_lexicon(LObj, SObj, WObj, l[u'Lexeme'], ed, annotation=l[u'English Gloss'])
            logger.echo(lex, True)
            
            # Create a cognate
            cog = Cognate.objects.create(lexicon=lex, cognateset=CogSet, source=SObj, editor=ed)
            cog.save()
            logger.echo(cog, True)
            
        print '\t + CogSet Entries:', CogSet.lexicon.count()
        
        logger.dump()