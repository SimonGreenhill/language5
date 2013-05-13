# -*- coding: utf-8 -*-
from optparse import make_option
from django.core.management.base import BaseCommand

from website.apps.lexicon.models import Lexicon


class Command(BaseCommand):
    args = 'split_entries --save'
    help = 'Splits Combined Lexical Entries'
    output_transaction = True
    option_list = BaseCommand.option_list + (
        make_option('--save',
            action='store_true',
            dest='save',
            default=False,
            help='Save changes'),
        )
        
    def _print(self, message):
        """
        Wrapper to print to stdout, if it exists
        
        (it won't exist if we're running tests)
        """
        if hasattr(self, 'stdout'):
            self.stdout.write(message)
    
    def find_combined(self):
        combined = []
        combined.extend(Lexicon.objects.filter(entry__icontains="/"))
        combined.extend(Lexicon.objects.filter(entry__icontains=","))
        return combined
    
    def split_and_replace(self, obj):
        if '/' in obj.entry:
            components = obj.entry.split("/")
        elif ',' in obj.entry:
            components = obj.entry.split(",")
        for c in components:
            c = c.strip()
            assert len(c) > 0, "Unable to split properly - zero length component"
            self._print("Splitting: %s -> %s" % (obj.entry, c))
            Lexicon.objects.create(
                language=obj.language, 
                word=obj.word,
                source=obj.source,
                editor=obj.editor,
                entry=c
            )
        # now delete old entry
        obj.delete()
        
    def handle(self, *args, **options):
        comb = self.find_combined()
        for obj in comb:
            self._print("Combined: %s" % obj.entry)
        
        if 'save' in options and options['save']:
            for obj in comb:
                self.split_and_replace(obj)
