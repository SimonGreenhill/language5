# -*- coding: utf-8 -*-
from reversion import revisions as reversion
from optparse import make_option
from django.core.management.base import BaseCommand

from website.apps.core.models import Language, Source
from website.apps.lexicon.models import Word, Lexicon


class Command(BaseCommand):
    args = 'split_entries --save [--word --language --source]'
    help = 'Splits Combined Lexical Entries'
    output_transaction = True
    
    def add_arguments(self, parser):
        parser.add_argument('--save',
            action='store_true',
            dest='save',
            default=False,
            help='Save changes'
        )
        parser.add_argument('--language',
            action='store',
            type='int',
            dest='language',
            default=False,
            help='Filter by language_id'
        )
        parser.add_argument('--word',
            action='store',
            type='int',
            dest='word',
            default=False,
            help='Filter by word_id'
        )
        parser.add_argument('--source',
            action='store',
            type='int',
            dest='source',
            default=False,
            help='Filter by source_id'
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
    
    def find_combined(self, language=None, word=None, source=None, ignore_protoforms=True):
        combined = []
        
        qset = Lexicon.objects.all().order_by('language')
        
        # filter on language if given a language.
        if language:
            qset = qset.filter(language=language)
        # filter on word if given a word.
        if word:
            qset = qset.filter(word=word)
        # filter on source if given a source.
        if source:
            qset = qset.filter(source=source)
        
        # remove protoforms 
        if ignore_protoforms:
            #qset = qset.exclude(entry__startswith="*")
            qset = qset.exclude(entry__regex=r'^\*\w+\(\w+[,/]\w+\)\w+')
            
        combined.extend(qset.filter(entry__icontains="/"))
        combined.extend(qset.filter(entry__icontains=", "))
        return combined
    
    def split_and_replace(self, obj, quiet=False):
        if '/' in obj.entry:
            components = obj.entry.split("/")
        elif ',' in obj.entry:
            components = obj.entry.split(",")
        pks = []
        for c in components:
            c = c.strip()
            assert len(c) > 0, "Unable to split properly - zero length component"
            self._print("Splitting: %s -> %s" % (obj.entry, c), quiet)
            with reversion.create_revision():
                o = Lexicon.objects.create(
                    language=obj.language, 
                    word=obj.word,
                    source=obj.source,
                    editor=obj.editor,
                    entry=c
                )
                reversion.set_comment("Automatic split_entries has created this from: %r" % obj.id)
                pks.append(o.id)
        
        # now delete old entry
        with reversion.create_revision():
            reversion.set_comment(
                "Automatic split_entries has moved this item to: %s" % ",".join([str(p) for p in pks])
            )
            obj.delete()
            
        
    def handle(self, *args, **options):
        language = options.get('language', None)
        word = options.get('word', None)
        source = options.get('source', None)
        
        if language:
            language = Language.objects.get(pk=language)
        if word:
            word = Word.objects.get(pk=word)
        if source:
            source = Source.objects.get(pk=source)
        
        comb = self.find_combined(language=language, word=word, source=source)
        
        for obj in comb:
            self._print(
                "L.%3d W.%3d S.%3d: \t %r" % (
                    obj.language.id,
                    obj.word.id,
                    obj.source.id, 
                    obj.entry,
                ),
                options.get('quiet', False)
            )
        
        if options.get('save', None):
            for obj in comb:
                self.split_and_replace(obj, options.get('quiet', False))
