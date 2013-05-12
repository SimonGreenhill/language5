# -*- coding: utf-8 -*-
from optparse import make_option
from django.core.management.base import BaseCommand

from website.apps.lexicon.models import Lexicon


class Command(BaseCommand):
    args = 'hygiene [empty]--delete'
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
    
    def delete(self, items):
        """Delete a list of records"""
        for obj in items:
            self._print('Deleting: %d - %s' % (obj.id, obj.entry))
            obj.delete()
            
    def handle(self, *args, **options):
        empties = self.find_empty()
        for obj in empties:
            self._print('Empty: %d - %s' % (obj.id, obj.entry))
        
        if 'delete' in options and options['delete']:
            self.delete(empties)
