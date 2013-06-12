# -*- coding: utf-8 -*-
import sys
import reversion
from optparse import make_option
from django.db import transaction
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from website.apps.lexicon.models import Word
from website.apps.entry.models import Wordlist, WordlistMember

class Command(BaseCommand):
    args = 'wordlist_name filename.txt'
    help = 'Creates a wordlist in `wordlist_name` from space delimited `filename.txt`'
    option_list = BaseCommand.option_list + (
        make_option('--run',
            action='store_true',
            dest='run',
            default=False,
            help='Run'),
        )
    
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
        errors = []
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
                    except ValueError as e:
                        raise ValueError("%s is not an integer, and there is an invalid order id" % order_id)
                
                try:
                    w = Word.objects.get(slug=line)
                except Word.DoesNotExist:
                    # we're going to crash anyway later. Just put a placeholder for now
                    w = None
                    errors.append(line)
                
                words[order_id] = w
                order_id += 1
        
        if len(errors):
            raise Word.DoesNotExist(
                "%d words don't exist: %s" % (len(errors), ", ".join(errors))
            )
            
        
        return words
        
    def handle(self, *args, **options):
        if len(args) != 2:
            print('Usage: ./manage.py create_wordlist <wordlist> </path/to/wordlist.txt>')
            quit()
        
        with open(args[1], 'rU') as handle:
            words = self.parse(handle)
        sys.stdout.write("%d words loaded from %s" % (len(words), args[1]))
        
        
        if 'run' in options and options['run']:
            ed = User.objects.get(pk=1)
            # create wordlist.
            with reversion.create_revision():
                wl = Wordlist.objects.create(
                    editor=ed, 
                    name=args[0]
                )
                wl.save()
            
            # go through words and add them to wordlist
            for order in sorted(words):
                with reversion.create_revision():
                    m = WordlistMember(wordlist=wl, word=words[order], order=order)
                    m.save()
            
            if wl.words.count() != len(words):
                raise AssertionError(
                    "Number of words in wordlist doesn't match expected (%d != %d)" % \
                    (wl.words.count(), len(words))
                )
            sys.stdout.write("Wordlist %s created with %d entries" % (wl, wl.words.count()))
        else:
            sys.stdout.write("Dry-run complete. Use --run to save changes. Rolling back.")
        