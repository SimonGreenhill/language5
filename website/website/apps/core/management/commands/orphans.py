# -*- coding: utf-8 -*-
from django.db.models import Count
from django.core.management.base import BaseCommand

from website.apps.core.models import Language, Source
from website.apps.lexicon.models import Word

class Command(BaseCommand):
    args = ''
    help = 'lists the orphaned data'
    output_transaction = True
    
    def handle(self, *args, **options):
        print('Languages not in a family:')
        for o in Language.objects.all().order_by('slug'):
            if len(o.family.all()) == 0:
                print(" - %s" % o.slug)
        print("")
        
        print('Languages with zero entries:')
        languages = Language.objects.annotate(count=Count('lexicon')).all()
        for o in languages.order_by('slug'):
            if o.count == 0:
                print(" - %s" % o.slug)
        print("")
        
        print('Sources with zero entries:')
        sources = Source.objects.annotate(count=Count('lexicon')).all()
        for o in sources.order_by('slug'):
            if o.count == 0:
                print(" - %s" % o.slug)
        print("")
        
        print('Words with zero entries:')
        words = Word.objects.annotate(count=Count('lexicon')).all()
        for o in words.order_by('slug'):
            if o.count == 0:
                print(" - %s" % o.slug)
        print("")
        
        
