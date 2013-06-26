# -*- coding: utf-8 -*-
import reversion
from django.db.models import Count
from optparse import make_option
from django.core.management.base import BaseCommand

from website.apps.lexicon.models import Word


class Command(BaseCommand):
    args = 'mergeword word1 word2 --save'
    help = 'Merges two words in the database'
    output_transaction = True
    option_list = BaseCommand.option_list + (
        make_option('--save',
            action='store_true',
            dest='save',
            default=False,
            help='Save changes to data rather than listing it'),
        )
    
    def _print(self, message):
        """
        Wrapper to print to stdout, if it exists

        (it won't exist if we're running tests)
        """
        if hasattr(self, 'stdout'):
            self.stdout.write(message)
    
    def handle(self, *args, **options):
        if len(args) != 2:
            raise IndexError("mergeword needs two slugs as arguments")
        
        # try get word 1
        try:
            w1 = Word.objects.get(slug=args[0])
        except Word.DoesNotExist:
            raise
            
        # try get word 2
        try:
            w2 = Word.objects.get(slug=args[1])
        except Word.DoesNotExist:
            raise
        
        for obj in w2.lexicon_set.all():
            self._print(obj)
            if 'save' in options and options['save']:
                with reversion.create_revision():
                    obj.word = w1
                    obj.save()
        
        # remove word 2
        if 'save' in options and options['save']:
            assert w2.lexicon_set.count() == 0
            with reversion.create_revision():
                w2.delete()
