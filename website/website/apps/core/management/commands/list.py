# -*- coding: utf-8 -*-
from optparse import make_option
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
        for o in Language.objects.all().order_by('slug'):
            alt = ",".join([p.name for p in o.alternatename_set.all()])
            if len(alt):
                alt = "[%s]" % alt
            
            print " ".join([
                '%3d' % o.id,
                '%3s' % o.isocode,
                o.slug.ljust(40),
                unicode(o).ljust(20),
                alt
            ]) 
    
    def list_families(self):
        for o in Family.objects.all().order_by('slug'):
            print " ".join([
                '%3d' % o.id,
                o.slug.ljust(40),
                unicode(o).ljust(20),
            ]) 
            
    def list_sources(self):
        for o in Source.objects.all().order_by('slug'):
            print " ".join([
                '%3d' % o.id,
                o.slug.ljust(40),
            ]) 
    
    def list_words(self):
        if Word is None:
            raise NotImplementedError("website.apps.lexicon not installed")
        for o in Word.objects.all().order_by('slug'):
            print " ".join([
                '%3d' % o.id,
                o.slug.ljust(40),
                unicode(o).ljust(20), 
            ])
            
    def handle(self, *args, **options):
        try:
            what = args[0]
        except ValueError:
            print self.args
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
