# -*- coding: utf-8 -*-
import reversion
from django.db.models import Count
from optparse import make_option
from django.core.management.base import BaseCommand

from website.apps.lexicon.models import Lexicon

try:
    from ftfy import fix_text
except ImportError:
    raise ImportError("Please install python-ftfy")

class Command(BaseCommand):
    args = 'hygiene [empty, tidy, dedupe] --save'
    help = 'Cleans Data from Database'
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
    
    def find_empty(self):
        """Find Empty Records"""
        empty = []
        empty.extend(Lexicon.objects.filter(entry=""))
        empty.extend(Lexicon.objects.filter(entry="-"))
        empty.extend(Lexicon.objects.filter(entry="--"))
        empty.extend(Lexicon.objects.filter(entry="---"))
        return empty
    
    def tidy(self):
        tidied = []
        for obj in Lexicon.objects.all():
            new = fix_text(obj.entry.strip(), fix_entities=True, normalization="NFKC", uncurl_quotes=True)
            if obj.entry != new:
                tidied.append((obj, new))
        return tidied
    
    def find_duplicates(self):
        dupes = Lexicon.objects.values('language', 'source', 'word', 'entry'
                    ).annotate(count=Count('entry')
                        ).filter(count__gte=2)
        objects = []
        for d in dupes:
            qset = Lexicon.objects.filter(language_id=d['language'], 
                                       source_id=d['source'],
                                       word_id=d['word'],
                                       entry__exact=d['entry'])
            assert len(qset) == d['count']
            objects.extend(qset[1:])
        return objects
        
        
    def delete(self, items):
        """Delete a list of records"""
        for obj in items:
            with reversion.create_revision():
                obj.delete()
    
    def handle(self, *args, **options):
        if len(args) == 0:
            args = ('empty', 'dedupe', 'tidy')
        
        if 't' in args or 'tidy' in args:
            tidier = self.tidy()
            for (obj, new) in tidier:
                self._print('Tidied: %s (%r) - %s (%r)' % (obj.entry, obj.entry, new, new))
                if 'save' in options and options['save']:
                    with reversion.create_revision():
                        obj.entry = new
                        obj.save()
        
        if 'e' in args or 'empty' in args or 'empties' in args:
            empties = self.find_empty()
            for obj in empties:
                self._print('Empty: %d - %r' % (obj.id, obj.entry))
            
            if 'save' in options and options['save']:
                self.delete(empties)
        
        if 'd' in args or 'dupes' in args or 'dedupe' in args:
            duplicates = self.find_duplicates()
            for obj in duplicates:
                self._print('Duplicate: %d/%d/%d/%d - %s, %s = %r' % (obj.id, 
                    obj.language.id, 
                    obj.source.id,
                    obj.word.id,
                    obj.language, obj.word, obj.entry))
            
            if 'save' in options and options['save']:
                self.delete(duplicates)
            
        