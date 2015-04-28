# -*- coding: utf-8 -*-
from django.db.models import Count
from optparse import make_option
from django.core.management.base import BaseCommand

from website.apps.core.models import Language, Family, Source
from website.apps.lexicon.models import Word, Lexicon
from website.apps.statistics import statistic

class Command(BaseCommand):
    args = ''
    help = 'summary of database'
    output_transaction = True
    
    def handle(self, *args, **options):
        print("# Families:")
        for o in Family.objects.all():
            print("\t".join([o.slug, '%d' % o.language_set.count()]))
        print("\n")
        
        print("# Languages:")
        for o in Language.objects.all():
            try:
                fam = o.family.all()[0].slug
            except IndexError:
                fam = "-"
            print("\t".join([o.slug, fam, '%d' % o.lexicon_set.count()]))
        print("\n")
        
        print("# Sources:")
        for o in Source.objects.all():
            print("\t".join([o.slug, '%d' % o.lexicon_set.count()]))
        print("\n")
        
        print("# Words:")
        for o in Word.objects.all():
            print("\t".join([o.slug, '%d' % o.lexicon_set.count()]))
        print("\n")
        
        print("# Statistics:")
        s = statistic.update(save=False)
        for label, value in s.items():
            print("*%s\t%d" % (label, value))