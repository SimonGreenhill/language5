# -*- coding: utf-8 -*-
import reversion
from optparse import make_option
from django.core.management.base import BaseCommand

from website.apps.lexicon.models import CognateSet


class Command(BaseCommand):
    args = 'display_cognate <id>'
    help = 'Displays a cognate set'
    output_transaction = True
    
    def handle(self, *args, **options):
        if len(args) != 1:
            raise IndexError("display_cognate needs a primary key")
        
        cogset = CognateSet.objects.get(id=int(args[0]))
        print("%d. /%s/ %s" % (cogset.id, cogset.protoform, cogset.gloss))
        for lex in cogset.lexicon.all():
            print(
                u" %5d.\t%20s\t%20s\t%s" % (
                    lex.id,
                    lex.language,
                    lex.word,
                    lex.entry,
                )
            )
        
