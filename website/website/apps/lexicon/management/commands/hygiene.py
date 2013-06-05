# -*- coding: utf-8 -*-
from django.db.models import Count
from optparse import make_option
from django.core.management.base import BaseCommand

from website.apps.lexicon.models import Lexicon


class Command(BaseCommand):
    args = 'hygiene --delete'
    help = 'Cleans Data from Database'
    output_transaction = True
    option_list = BaseCommand.option_list + (
        make_option('--delete',
            action='store_true',
            dest='delete',
            default=False,
            help='Delete dirty data rather than listing it'),
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
            obj.delete()
            
    def handle(self, *args, **options):
        empties = self.find_empty()
        duplicates = self.find_duplicates()
        
        for obj in empties:
            self._print('Empty: %d - %r' % (obj.id, obj.entry))
        for obj in duplicates:
            self._print('Duplicate: %d - %s, %s = %r' % (obj.id, obj.language, obj.word, obj.entry))
        
        if 'delete' in options and options['delete']:
            self.delete(empties)
            self.delete(duplicates)
            
        