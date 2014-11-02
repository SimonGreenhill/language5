# -*- coding: utf-8 -*-
import reversion
import unicodedata
from django.db.models import Count
from optparse import make_option
from django.core.management.base import BaseCommand
from collections import Counter
from website.apps.core.models import Source


class Command(BaseCommand):
    args = 'ipatable source'
    help = 'Prints the IPA table for the given source'
    output_transaction = True
    
    def handle(self, *args, **options):
        if len(args) != 1:
            raise IndexError("ipatable needs a source slug")
        
        try:
             SObj = Source.objects.get(slug=args[0])
        except Source.DoesNotExist:
            raise Source.DoesNotExist(u"Unable to find {}".format(args[0]))
        
        chars = Counter()
        total = 0
        for obj in SObj.lexicon_set.all():
            chars.update(obj.entry)
            total += len(obj.entry)
        assert total == sum(chars.values())
        
        for char in sorted(chars):
            u = unicodedata.name(char)
            print(u"\t".join([char, '%d' % chars[char], u.ljust(50), u"?"]))
