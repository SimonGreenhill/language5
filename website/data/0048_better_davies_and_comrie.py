#!/usr/bin/env python
#coding=utf-8
import os
import re
import reversion

from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from website.apps.core.models import Source, Language
from website.apps.lexicon.models import Lexicon, Word, CognateSet, Cognate

from openpyxl import load_workbook

filename = os.path.join(os.environ['IMPORTER_DATAROOT'], '0011_davies_and_comrie.xlsx')
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

word_map = {
    'his back': 'back',
    'his shoulder': 'shoulder',
    'his forehead': 'forehead',
    'his thumb': 'thumb',
    'his leg': 'leg',
    'his heart': 'heart',
    'his bone': 'bone',
    'his blood': 'blood',
    'his father': 'father',
    'his mother': 'mother',
    'warm, hot': 'warm',
    'he says': 'to-say',
    'he hears': 'to-hear',
    'he dies': 'to-die',
    'it burns': 'to-burn',
    'he hits': 'to-hit',
    'he laughs': 'to-laugh',
    'no': 'no-not',
    'I': 'i',
    'he': 'he-she',
    'we two (excl)': 'we-two-excl',
    'you two': 'you-pl-dual',
    'they two': 'they-dual',
    'we (pl. excl.)': 'we-pl-excl',
    'you (plural)': 'you-pl',
    'they (plural)': 'they',
    'thou': 'you',
}




def find_cognate(entry):
    cognates = []
    is_cognate = re.compile(r"""(.*)\s+(\d+)$""")
    is_cognate_2 = re.compile(r"""(.*)\s+(\d+/\d+)$""")
    is_cognate_3 = re.compile(r"""(.*)\s+(\d+/\d+/\d+)$""")
    
    if is_cognate.match(entry):
        entry, cognates = is_cognate.findall(entry)[0]
        cognates = [int(cognates)]
    elif is_cognate_2.match(entry):
        entry, cognates = is_cognate_2.findall(entry)[0]
        cognates = [int(c) for c in cognates.split("/")]
    elif is_cognate_3.match(entry):
        entry, cognates = is_cognate_3.findall(entry)[0]
        cognates = [int(c) for c in cognates.split("/")]
    else:
        pass
    return (entry, cognates)


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
    cognate = []
    for i in item.split(" / "):
        i = i.strip()
        i, cog = find_cognate(i)
        cognate.extend(cog)
        
        if '/' in i:
            raise ValueError("ERROR: %s" % i)
        
        if len(cog):
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
SObj = Source.objects.get(pk=68)

# REMOVE lexicon
with reversion.create_revision():
    for lex in Lexicon.objects.filter(source=SObj):
        lex.delete()
    for cset in CognateSet.objects.filter(source=SObj):
        cset.delete()
    for cog in Cognate.objects.filter(source=SObj):
        cog.delete()


wb = load_workbook(filename=filename)
w = wb.worksheets[0]

header = [_.value for _ in w.columns[0]]

counter = 0
for i in range(1, w.get_highest_column()):
    values = [_.value for _ in w.columns[i]]
    values = dict(zip(header, values))
    # get word, yes really.
    source_gloss = values.pop(u'Language')
    source_gloss = source_gloss.strip()
    print i, source_gloss
    
    if source_gloss in word_map:
        word = word_map[source_gloss]
    else:
        word = slugify(source_gloss)
    
    # note get_or_create does not work when transaction management is on...
    try:
        WObj = Word.objects.get(slug=word)
    except Word.DoesNotExist:
        raise ValueError("Unable to find: %s :: %s" % (source_gloss, word))
        
        #WObj = Word.objects.create(word=word, slug=slugify(word), editor=ed)
        #WObj.save()
    
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
            for entry, cognates in item:
                counter += 1
                print "\t", counter, 'Lexicon', language.ljust(20), entry.ljust(30), cognates
                lex = Lexicon.objects.create(
                    language=LObj, 
                    source=SObj,
                    source_gloss=source_gloss,
                    word=WObj, 
                    entry=entry, 
                    annotation='', 
                    editor=ed
                )
                lex.save()
                
                for cognate in cognates:
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
                comment="Davies & Comrie 1985: %d" % cogid,
                quality='1', # published
                editor=ed
            )
            CogSet.save()
            counter += 1
            print "\t", counter, 'CognateSet', CogSet.comment
            for m in members:
                counter += 1
                cog = Cognate.objects.create(lexicon=m, cognateset=CogSet, source=SObj, editor=ed)
                cog.save()
                print "\t", counter, 'Cognate', cog, m


print '%d objects created!' % counter