# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from website.apps.core.models import Language, Family, Source

try:
    from website.apps.lexicon.models import Word
except ImportError:
    # not installed
    Word = None
    

class Command(BaseCommand):
    args = 'list language/source/word/family'
    help = 'Lists the entries in the database'
    output_transaction = True
    
    def list_languages(self):
        print("\t".join([
            "ISO", "Slug", "Language", "Families", "NLexicon", "Classification"
        ]))
        for o in Language.objects.all().order_by('slug'):
            print("\t".join([
                '%3s' % o.isocode,
                o.slug,
                o.ljust(20),
                ",".join([f.slug for f in o.family.all()]),
                "%d" % o.lexicon_set.count(),
                o.classification
            ]))
    
    def list_families(self):
        print("\t".join(["Slug", "Family", "NLanguages"]))
        for o in Family.objects.all().order_by('slug'):
            print "\t".join([
                o.slug,
                o,
                '%d' % o.language_set.count()
            ])
            
    def list_sources(self):
        print("\t".join([
            "Slug", "Source", "Year", "NLexicon", "NCognateSets"
        ]))
        for o in Source.objects.all().order_by('slug'):
            print("\t".join([
                o.slug,
                o,
                o.year,
                '%d' % o.lexicon_set.count(),
                '%d' % o.cognate_set.count()
            ]))
    
    def list_words(self):
        print("\t".join(["Slug", "Word", "NLexicon"]))
        for o in Word.objects.all().order_by('slug'):
            print("\t".join([
                o.slug,
                o,
                '%d' % o.lexicon_set.count()
            ]))
     
    def handle(self, *args, **options):
        try:
            what = args[0]
        except ValueError:
            quit()
        
        if what in ('languages', 'language', 'lang', 'l'):
            self.list_languages()
        elif what in ('sources', 'source', 's'):
            self.list_sources()
        elif what in ('families', 'family', 'f'):
            self.list_families()
        elif what in ('words', 'word', 'w'):
            self.list_words()
        else:
            raise ValueError("Unknown list field: %s" % what)
