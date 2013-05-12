# -*- coding: utf-8 -*-
from optparse import make_option
from django.core.management.base import BaseCommand

from website.apps.core.models import Language, Source

try:
    from website.apps.lexicon.models import Lexicon, Word
except ImportError:
    # not installed
    Lexicon, Word = None, None


class Command(BaseCommand):
    args = 'search language/source/word/lexicon query'
    help = 'Searches Database'
    output_transaction = True
    
    def search_isocodes(self, query):
        for i in Language.objects.select_related().filter(isocode__iexact="%s" % query):
            print " ".join([
                '%d' % i.id,
                i.language.ljust(20),
                i.isocode.ljust(20), 
                i.classification
            ])
    
    def search_languages(self, query):
        for i in Language.objects.select_related().filter(language__icontains="%s" % query, isocode__iexact="%s" % query):
            print " ".join([
                '%d' % i.id,
                i.language.ljust(20),
                i.isocode.ljust(20), 
                i.classification
            ]) 
    
    def search_sources(self, query):
        for i in Source.objects.select_related().filter(author__icontains="%s" % query):
            print " ".join([
                '%d' % i.id,
                i.author.ljust(20),
                '%d' % i.year, 
                i.reference
            ]) 
    
    def search_lexicon(self, query):
        if Lexicon is None:
            raise NotImplementedError("website.apps.lexicon not installed")
        for i in Lexicon.objects.select_related().filter(entry__icontains="%s" % query):
            print " ".join([
                '%d' % i.id,
                str(i.language).ljust(20),
                str(i.source).ljust(20), 
                str(i.word).ljust(10), 
                i.entry
            ])
    
    def search_words(self, query):
        if Word is None:
            raise NotImplementedError("website.apps.lexicon not installed")
        for i in Word.objects.select_related().filter(word__icontains="%s" % query):
            print " ".join([
                '%d' % i.id,
                i.word.ljust(20),
                i.full.ljust(20), 
            ])
            
    def handle(self, *args, **options):
        try:
            what, query = args
        except ValueError:
            print self.args
            quit()
        
        if what in ('languages', 'language', 'lang', 'l'):
            self.search_languages(query)
        elif what in ('sources', 'source', 's'):
            self.search_sources(query)
        elif what in ('isocode', 'iso', 'i'):
            self.search_isocodes(query)
        elif what in ('lexicon', 'lex',):
            self.search_lexicon(query)
        elif what in ('words', 'word', 'w'):
            self.search_words(query)
        else:
            raise ValueError("Unknown search field: %s" % what)
