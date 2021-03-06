# -*- coding: utf-8 -*-
from reversion import revisions as reversion
from django.db.models import Count
from optparse import make_option
from django.core.management.base import BaseCommand

from website.apps.lexicon.models import Word


class Command(BaseCommand):
    args = 'mergeword destination source --save'
    help = 'Merges two words in the database'
    output_transaction = True
    
    
    def add_arguments(self, parser):
        parser.add_argument('--save',
            action='store_true',
            dest='save',
            default=False,
            help='Save changes to data rather than listing it'
        )
        parser.add_argument('--quiet',
            action='store_true',
            dest='save',
            default=False,
            help='be quiet'
        )
    
    def _print(self, message, quiet=False):
        """
        Wrapper to print to stdout, if it exists
        
        (it won't exist if we're running tests)
        """
        if not quiet and hasattr(self, 'stdout'):
            self.stdout.write(message)
    
    def handle(self, *args, **options):
        if len(args) != 2:
            raise IndexError("mergeword needs two slugs as arguments: mergeword destination source")
        
        if 'save' in options and options['save']:
            dryrun = False
        else:
            dryrun = True
            self._print(
                "*** DRY RUN! Use --save to save changes! ***",
                options.get('quiet', False)
            )
        
        # try get word 1
        try:
            dest = Word.objects.get(slug=args[0])
        except Word.DoesNotExist:
            raise Word.DoesNotExist(u"Unable to find {}".format(args[0]))
            
        # try get word 2
        try:
            source = Word.objects.get(slug=args[1])
        except Word.DoesNotExist:
            raise Word.DoesNotExist(u"Unable to find {}".format(args[1]))
        
        for obj in source.lexicon_set.all():
            self._print(
                u"Moving {} to {}".format(obj, dest),
                options.get('quiet', False)
            )
            if not dryrun:
                with reversion.create_revision():
                    obj.word = dest
                    obj.save()
        
        # remove word 2
        if not dryrun:
            assert source.lexicon_set.count() == 0
            with reversion.create_revision():
                self._print(
                    "Deleting Word {}".format(source),
                    options.get('quiet', False)
                )
                source.delete()
        else:
            self._print(
                "*** DRY RUN! Use --save to save changes! ***",
                options.get('quiet', False)
            )
            
