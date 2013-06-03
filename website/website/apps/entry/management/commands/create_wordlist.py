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
    
    def parse(self, handle):
        """Reads a filename. Ordering is set to order in file
        
        File format: 
        
            <word>
            hand
            leg
            foot
            # a comment -- ignored
            ...
        
        Or:
        
            1 hand
            2 leg
            3 foot
            ...
        """
        words = {}
        order_id = 1
        for line in handle.readlines():
            line = line.strip()
            if len(line) == 0:
                continue
            elif line.startswith("#"):
                continue
            else:
                if " " in line:
                    order_id, line = [x.strip() for x in line.split(" ", 1)]
                    try:
                        order_id = int(order_id) 
                    except ValueError:
                        raise ValueError("%s is not an integer, and there is an invalid order id" % order_id)
                
                try:
                    w = Word.objects.get(slug=line)
                except Word.DoesNotExist:
                    raise Word.DoesNotExist("'%r' does not exist - create it!" % line)
                
                words[order_id] = w
                order_id += 1
        return words
        
    def handle(self, *args, **options):
        if len(args) != 2:
            print('Usage: ./manage.py create_wordlist <wordlist> </path/to/wordlist.txt>')
            quit()
        
        with open(args[1], 'rU') as handle:
            words = self.parse(handle)
        
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
