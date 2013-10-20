#!/usr/bin/env python
from django.contrib.auth.models import User

# import models
from website.apps.core.models import Source, Language
from website.apps.lexicon.models import CorrespondenceSet, Correspondence
import codecs
import json
import os

# ERROR Ambe-Dofo

# ERROR Gena
# ERROR Karoto

SKIP = ['pBinAmb', ]


LANGUAGE_SLUGS = {
    'pBin': 'proto-binandere',    
    'pCstBin': 'proto-coastal-binandere',
    'pNucBin': 'proto-nuclear-binandere',
    'pSBin': 'proto-south-binandere',
    'pNBin': 'proto-north-binandere',
    'pOro': 'proto-orokaiva',
    'pBar': 'proto-baruga',
    'pZM': 'proto-zia-mawae',

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

ed = User.objects.get(pk=1) # get editor
s = Source.objects.get(slug=SOURCE_SLUG) # get source

#print s
datafile = os.path.join(os.environ['IMPORTER_DATAROOT'], '0010_binandere_correspondences.json')
assert os.path.isfile(datafile), "Can't find datafile: %s" % datafile

with codecs.open(datafile, 'rU', encoding="utf8") as handle:
    data = json.load(handle)


protobinandere = data.get('pBin')
PBin = Language.objects.get(slug='proto-binandere')

del(data['pBin'])
for key in protobinandere:
    value = protobinandere[key] 
    comment = 'Smallhorn (2011) Proto-Binandere %s' % value
    
    # create corrset
    corrset = CorrespondenceSet.objects.create(
        editor=ed,
        source=s,
        comment=comment
    ) 
    corrset.save()
    print corrset.comment, ':'
    
    # add Pbin to corrset
    corr = Correspondence.objects.create(
        language=PBin,
        corrset=corrset,
        rule=value,
        editor=ed
    )
    corr.save()
    print ' - ', corr.language, corr.rule

    # and the other languages
    for language in data:
        if language in SKIP:
            continue
        try:
            slug = LANGUAGE_SLUGS[language]
        except:
            raise ValueError("Unable to find slug for %s" % language)
        
        Lobj = Language.objects.get(slug=slug)

        corr = Correspondence.objects.create(
            language=Lobj,
            corrset=corrset,
            rule=data[language][key],
            editor=ed
        )
        corr.save()
        print ' - ', corr.language, corr.rule
    
    print
