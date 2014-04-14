#!/usr/bin/env python
import reversion
from website.apps.lexicon.models import Word, Lexicon

def cleanup(wordslug, newslug, search=None):
    try:
        old = Word.objects.get(slug=wordslug)
    except Word.DoesNotExist:
        raise Word.DoesNotExist("Unable to find: %s" % wordslug)
    try:
        new = Word.objects.get(slug=newslug)
    except Word.DoesNotExist:
        raise Word.DoesNotExist("Unable to find: %s" % newslug)
    
    for lex in Lexicon.objects.filter(word=old):
        if lex.annotation == search:
            with reversion.create_revision():
                lex.word = new
                lex.save()
                print('  >> %5d \t %20s \t-> %20s' % (lex.id, old, new))
                

#cleanup('face-forehead', 'face', 'face')
cleanup('leg-foot', 'leg', 'leg')
cleanup('leg-foot', 'foot', 'foot')
cleanup('arm-hand', 'arm', 'arm')
cleanup('arm-hand', 'hand', 'hand')
cleanup('chin-jaw', 'chin', 'chin')
cleanup('chin-jaw', 'jaw', 'jaw')
cleanup('fat-grease', 'fat', 'fat')


