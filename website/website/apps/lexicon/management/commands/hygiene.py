# -*- coding: utf-8 -*-
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
    
    def handle(self, *args, **options):
        self.dirty = []
        self.dirty.extend(Lexicon.objects.filter(entry=""))
        self.dirty.extend(Lexicon.objects.filter(entry="-"))
        self.dirty.extend(Lexicon.objects.filter(entry="--"))
        self.dirty.extend(Lexicon.objects.filter(entry="---"))
        
        if 'delete' in options and options['delete']:
            for d in self.dirty:
                d.delete()
                if hasattr(self, 'stdout'):
                    self.stdout.write('Deleted: %d - %s' % (d.id, d.entry))
        else:
            for d in self.dirty:
                if hasattr(self, 'stdout'):
                    self.stdout.write('Dirty: %d - %s' % (d.id, d.entry))