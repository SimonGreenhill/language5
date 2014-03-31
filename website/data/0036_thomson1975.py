#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs

from django.contrib.auth.models import User
from website.apps.core.models import Language, Source, AlternateName, Family
from website.apps.lexicon.models import Word, Lexicon

# importer sets some variables
import os
DIRNAME = os.path.join(os.environ['IMPORTER_DATAROOT'], '0036_thomson1975')

REFERENCE = """
Thomson NP. 1975. The dialects of Magi. In R. Conrad et al. Eds. Papers in New Guinea Linguistics No. 18. Canberra: Pacific Linguistics, pp. 37-90.
"""

CONVERT = {
    # temp word slug -> actual slug
    'forehead': u'face-forehead',
    'we-two': 'we-dual',
    'jaw': 'chin-jaw',
    'betel-nut': 'betelnut',
    'fat': 'fat-grease',
    'leg': 'leg-foot',
    'sore': 'sore-wound',
    'pond': 'lake',
    'string': 'rope',
    'hungry': 'to-be-hungry',
    'to-stand-up': 'to-stand',
    'to-sit-down': 'to-sit',
    'to-chop': 'to-chop-cut-down',
    'you(s)': 'you-sg',
    'to-be-afraid': 'afraid',
    'together-with': 'with',
    'to-pour': 'to-pour-out',
    'pain': 'painful-sick',
    'sick': 'painful-sick',
    'body-hair': 'hair-body',
    'joke': 'to-joke',
    'clothes': 'cloth-clothes',
    'stop': 'to-stop',
    'to-buy': 'to-buy-sell-barter',
    'he': 'he-she',
    'arm': 'arm-hand',
    'come-quickly': 'to-come',
    'to-look-for': 'to-look',
    'blunt': 'dull',
    'piece-of-wood': 'short-piece-wood',
    'ripe-banana': 'banana',
    'to-put-down': 'to-put',
    'to-draw-water': 'draw-water-carry',
    'fly': 'to-fly',

    
    #'sole-of-foot': palm-of-hand-sole-of-foot,
    # 'palm-of-hand'
}

ANNOTATE = {
    'together-with': 'together with',
    'pain': 'pain',
    'sick': 'sick',
    'to-buy-sell-barter': 'to buy',
    'ripe-banana': 'ripe banana',
}


# get editor
ed = User.objects.get(pk=1)

SObj = Source.objects.create(year=1975, author="Thomson", slug="thomson1975",
                          reference=REFERENCE.strip().lstrip(), bibtex="", comment="",
                          editor=ed)

TNG = Family.objects.get(slug="transnewguinea")



for filename in os.listdir(DIRNAME):
    if not filename.endswith('.txt'):
        continue
        
    ffilename = os.path.join(DIRNAME, filename)
    
    dialect = filename.replace(".txt", '').replace("magi-", "").title()
    
    # create language
    LObj = Language.objects.create(
        language='Mailu',
        dialect=dialect,
        slug = filename.replace('.txt', '').replace('magi-', 'mailu-'),
        isocode = "mgu",
        classification = "Trans-New Guinea, Southeast Papuan, Mailuan",
        editor=ed
    )
    
    LObj.family.add(TNG)
    LObj.save()
    
    a = AlternateName.objects.create(
        language=LObj, editor=ed, name="Magi %s" % dialect.title(), slug="magi-%s" % dialect
    )
    
    with codecs.open(ffilename, 'rU', encoding="utf8") as handle:
        for line in handle.readlines():
            line = line.strip()
            if line.startswith("#"):
                continue
            elif len(line) == 0:
                continue
            else:
                slug, entry = line.split(" ", 1)
                if slug in ANNOTATE:
                    annot = ANNOTATE[slug]
                else:
                    annot = ""
                
                if slug in CONVERT:
                    slug = CONVERT[slug]
                
                entry = entry.strip()
                if entry == u'-' or entry == u'':
                    continue
                entry = entry.replace("?", u"ʔ")
                
                WObj = Word.objects.get(slug=slug)
                lex = Lexicon.objects.create(
                    language=LObj,
                    source=SObj,
                    word=WObj, 
                    entry=entry, 
                    annotation=annot,
                    editor=ed
                )
                print LObj, WObj, lex
                