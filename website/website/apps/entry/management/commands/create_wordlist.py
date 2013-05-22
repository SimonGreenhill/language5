# -*- coding: utf-8 -*-
import json
import codecs
from django.db import transaction
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from website.apps.lexicon.models import Word
from website.apps.entry.models import Wordlist, WordlistMember

class Command(BaseCommand):
    args = 'wordlist_name filename.txt'
    help = 'Creates a wordlist in `wordlist_name` from space delimited `filename.txt`'
    
    def readfilename(self, filename):
        """Reads a filename. Ordering is set to order in file
        
        <word>
        hand
        leg
        foot
        # a comment -- ignored
        ...
        """
        words = {}
        order_id = 1
        with open(filename, 'rU') as handle:
            for line in handle.readlines():
                line = line.strip()
                if len(line) == 0:
                    continue
                elif line.startswith("#"):
                    continue
                else:
                    try:
                        w = Word.objects.get(slug=line)
                    except Word.DoesNotExist:
                        raise Word.DoesNotExist("'%s' does not exist - create it!" % w)
                    
                    words[order_id] = w
                    order_id += 1
        return words
        
    def handle(self, *args, **options):
        words = self.readfilename(args[1])
        
        ed = User.objects.get(pk=1)
        
        # create wordlist.
        wl = Wordlist.objects.create(
            editor=ed, 
            name=args[0]
        )
        wl.save()
        
        # go through words and add them to wordlist
        for order in sorted(words):
            m = WordlistMember(wordlist=wl, word=words[order], order=order)
            m.save()
        
        assert wl.words.count() == order
        print("Wordlist %s created with %d entries" % (wl, order))
