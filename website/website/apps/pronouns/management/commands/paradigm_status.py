# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from website.apps.pronouns.models import Paradigm

class Command(BaseCommand):
    args = ''
    help = 'Displays the status of all the paradigms in the Database'
    
    def handle(self, *args, **options):
        completed, pcount = 0, 0
        for pdm in Paradigm.objects.all().order_by('id'):
            missing, total = 0, 0
            for p in pdm.pronoun_set.all():
                entries = p.entries.count()
                if entries == 0:
                    missing += 1
                total += entries
                
            try:
                family = pdm.language.family.all()[0].slug
            except IndexError:
                family = '?'
                
            print("\t".join([
                '%4d' % pdm.id,
                pdm.language.isocode,
                pdm.language.slug.ljust(30),
                family.ljust(20),
                '%3d' % total,
                '%3d' % missing,
                'COMPLETE' if missing == 0 else ''
            ]))
            
            if missing == 0:
                completed += 1
            pcount += 1
        
        print("\nCompleted: %d/%d" % (completed, pcount))
