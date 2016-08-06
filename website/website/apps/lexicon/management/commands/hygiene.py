# -*- coding: utf-8 -*-
from reversion import revisions as reversion
from django.db.models import Count
from optparse import make_option
from django.core.management.base import BaseCommand

from website.apps.core.models import Language
from website.apps.lexicon.models import Lexicon

class Command(BaseCommand):
    args = 'hygiene [empty, tidy, dedupe, star] --save [--quiet]'
    help = 'Cleans Data from Database'
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

    def find_empty(self):
        """Find Empty Records"""
        empty = []
        empty.extend(Lexicon.objects.filter(entry=""))
        empty.extend(Lexicon.objects.filter(entry="-"))
        empty.extend(Lexicon.objects.filter(entry="--"))
        empty.extend(Lexicon.objects.filter(entry="---"))
        return empty
    
    def find_unstarred(self):
        unstarred = []
        for proto in Language.objects.filter(language__startswith='Proto'):
            unstarred.extend(proto.lexicon_set.exclude(entry__startswith='*'))
        return unstarred
    
    def tidy(self):
        try:
            from ftfy import fix_text
        except ImportError:
            raise ImportError("Please install python-ftfy")
        
        tidied = []
        for obj in Lexicon.objects.all():
            new = fix_text(obj.entry.strip(), fix_entities=True, normalization="NFKC", uncurl_quotes=True)
            if obj.entry != new:
                tidied.append((obj, new))
        return tidied
    
    def find_duplicates(self):
        dupes = Lexicon.objects.values('language', 'source', 'word', 'entry')
        dupes = dupes.annotate(count=Count('entry')).filter(count__gte=2)
        
        objects = []
        for d in dupes:
            qset = Lexicon.objects.filter(
                language_id=d['language'], 
                source_id=d['source'],
                word_id=d['word'],
                entry__exact=d['entry']
            ).order_by('id')
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
            args = ('empty', 'dedupe', 'tidy', 'star')
        
        if 't' in args or 'tidy' in args:
            tidier = self.tidy()
            for (obj, new) in tidier:
                self._print(
                    'Tidied: %s (%r) - %s (%r)' % (obj.entry, obj.entry, new, new),
                    options.get('quiet', False)
                        
                )
                if 'save' in options and options['save']:
                    with reversion.create_revision():
                        obj.entry = new
                        obj.save()
        
        if 'e' in args or 'empty' in args or 'empties' in args:
            empties = self.find_empty()
            for obj in empties:
                self._print(
                    'Empty: %d - %r' % (obj.id, obj.entry),
                    options.get('quiet', False)
                )
            
            if 'save' in options and options['save']:
                self.delete(empties)
        
        if 'd' in args or 'dupes' in args or 'dedupe' in args:
            duplicates = self.find_duplicates()
            for obj in duplicates:
                self._print(
                    'Duplicate: %d/%d/%d/%d - %s, %s = %r' % (obj.id, 
                        obj.language.id, 
                        obj.source.id,
                        obj.word.id,
                        obj.language, obj.word, obj.entry),
                        options.get('quiet', False)
                    )
            
            if 'save' in options and options['save']:
                self.delete(duplicates)
                
        if 's' in args or 'star' in args:
            unstarred_forms = self.find_unstarred()
            for obj in self.find_unstarred():
                new = '*%s' % obj.entry
                self._print(
                    'Starred: %s - %s (%r) - %s (%r)' % (obj.language, obj.entry, obj.entry, new, new),
                    options.get('quiet', False)
                )
                if 'save' in options and options['save']:
                    with reversion.create_revision():
                        obj.entry = new
                        obj.save()
                