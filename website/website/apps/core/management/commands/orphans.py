# -*- coding: utf-8 -*-
from django.db.models import Count
from optparse import make_option
from django.core.management.base import BaseCommand

from website.apps.core.models import Language, Family, Source
from website.apps.lexicon.models import Word

class Command(BaseCommand):
    args = ''
    help = 'lists the orphaned data'
    output_transaction = True
    
    def handle(self, *args, **options):
        print 'Languages not in a family:'
        for o in Language.objects.all().order_by('slug'):
            if len(o.family.all()) == 0:
                print " - ", o.slug
        print
        
        print 'Languages with zero entries:'
        for o in Language.objects.annotate(count=Count('lexicon')).all().order_by('slug'):
            if o.count == 0:
                print " - ", o.slug
        print
        
        print 'Sources with zero entries:'
        for o in Source.objects.annotate(count=Count('lexicon')).all().order_by('slug'):
            if o.count == 0:
                print " - ", o.slug
        print

        print 'Words with zero entries:'
        for o in Word.objects.annotate(count=Count('lexicon')).all().order_by('slug'):
            if o.count == 0:
                print " - ", o.slug
        print
        
        