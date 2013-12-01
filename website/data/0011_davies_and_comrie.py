#!/usr/bin/env python
#coding=utf-8
import os
import re

from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from website.apps.core.models import Source, Language
from website.apps.lexicon.models import Lexicon, Word, CognateSet, Cognate

from openpyxl import load_workbook

filename = os.path.join(os.environ['IMPORTER_DATAROOT'], '0011_davies_and_comrie.xlsx')
is_cognate = re.compile(r"""\s+?(\d+?)$""")
languages = {
    'Bisorio': 'bisorio',
    'Iniai': 'bisorio-iniai',
    'Lembena': 'lembena',
    'Kyaka Enga': 'kyaka',
    'Pinai 1': 'pinai-hagahai-wakadadap',
    'Pinai 2': 'pinai-hagahai',
    'Wiyaw': 'wiyaw',
    'Aramo': 'aramo',
    'Kobon': 'kobon',
    'Rao': 'rao',
    'Miyak': 'miyak',
    'Yimas': 'yimas',
    'Alamblak': 'alamblak',
    'Banaro': 'banaro',
    'Lapalama Enga 1': 'enga-lapalama',
    'Lapalama Enga 2': 'enga-lapalama',
    'Wapi Enga': 'enga-wapi',
    'Laiagam Enga': 'enga-laiagam',
    'Sari Enga': 'enga-sari',
    'Nangenuwetan': 'nangenuwetan',
    'Kyaimbarang': 'kyaimbarang',
    'Alfendio': 'alfendio',
    'Yariba': 'lembena-yariba',
    'Maibi': 'lembena-maibi',
}


def process_item(item):
    if item is None:
        # completely empty
        return None
    assert unicode(item)
    assert item.encode('utf8')
    item = item.strip()
    
    if item == '/' or item == '\\':
        # Marked as empty
        return None
    
    if item.startswith("''"):
        raise ValueError("ERROR 1: %s" % item)
    
    # fail if I need to check it.
    if 'check' in item:
        raise ValueError("CHECK 1: %s" % item)
    if 'superscript' in item:
        raise ValueError("CHECK 3: %s" % item)
    
    # start processing properly.
    items = []
    cognate = None
    for i in item.split(" / "):
        i = i.strip()
        # get cognate
        cog = is_cognate.findall(i)
        if len(cog):
            if cognate is not None and int(cog[0]) != cognate:
                print 'ERROR', item
                raise ValueError(u"Duplicate cognate set for same item!: {}".format(item))
            
            cognate = int(cog[0])
            i = is_cognate.sub('', i)
            i = i.strip()
            
            # make sure that we haven't assigned a cognate set i.e. an integer 
            # to something that should be a reflex.
            try:
                int(i)
            except:
                pass
            else:
                raise ValueError(u'%r :: %s :: %r' % (item, cog, i))
            
            if len(i) == 0:
                raise ValueError(u'%r :: %s :: %r' % (item, cog, i))
            
            
        items.append(i)
    
    return [(i, cognate) for i in items]

# ------------------------------- #


# get editor
ed = User.objects.get(pk=1)
# create source
SObj = Source.objects.create(
        year=1985, 
        author="Davies and Comrie", slug="davies_and_comrie1985",
        reference="Davies & Comrie. 1985. A linguistic survey of the Upper Yuat. In Adams et al. Papers in New Guinea Linguistics No. 22, pp. 275-312", 
        bibtex="", comment="",
        editor=ed)

wb = load_workbook(filename=filename)
w = wb.worksheets[0]

header = [_.value for _ in w.columns[0]]

counter = 0
for i in range(1, w.get_highest_column()):
    values = [_.value for _ in w.columns[i]]
    values = dict(zip(header, values))
    # get word, yes really.
    word = values.pop(u'Language')
    print i, word
    
    # note get_or_create does not work when transaction management is on...
    try:
        WObj = Word.objects.get(slug=slugify(word))
    except Word.DoesNotExist:
        WObj = Word.objects.create(word=word, slug=slugify(word), editor=ed)
        WObj.save()
    
    cognate_sets = {}
    
    for language in sorted(values):
        if language is None:
            continue
            
        lslug = languages[language]
        try:
            LObj = Language.objects.get(slug=lslug)
        except Language.DoesNotExist:
            LObj = Language.objects.create(language=language, slug=lslug, editor=ed)
            LObj.save()
            # FOR DEBUGGING ONLY ON LOCAL SITE. PRODUCTION SHOULD 
            # HAVE THIS LANGUAGE ALREADY CREATED!
            print 'ERROR: I should not have needed to create %s' % language
        
        item = process_item(values[language])
        if item is not None:
            for entry, cognate in item:
                counter += 1
                print "\t", counter, 'Lexicon', language.ljust(20), entry.ljust(30), cognate
                lex = Lexicon.objects.create(
                    language=LObj, 
                    source=SObj,
                    word=WObj, 
                    entry=entry, 
                    annotation='', 
                    editor=ed
                )
                lex.save()        
                
                cognate_sets[cognate] = cognate_sets.get(cognate, [])
                cognate_sets[cognate].append(lex)
                
    
    # Add things with more than one entry to a cognate set
    for cogid, members in cognate_sets.items():
        if len(members) > 1:
            # Add protoform --> <?>
            CogSet = CognateSet.objects.create(
                protoform='?',
                gloss=word,
                source=SObj,
                comment="",
                quality='1', # published
                editor=ed
            )
            CogSet.save()
            counter += 1
            print "\t", counter, 'CognateSet', CogSet
            for m in members:
                counter += 1
                cog = Cognate.objects.create(lexicon=m, cognateset=CogSet, source=SObj, editor=ed)
                cog.save()
                print "\t", counter, 'Cognate', cog, m


print '%d objects created!' % counter