# -*- coding: utf-8 -*-
from optparse import make_option
from django.core.management.base import BaseCommand

from website.apps.core.models import Language, Family

class Command(BaseCommand):
    args = ''
    help = 'lists the languages who do not belong to a language'
    output_transaction = True
    
    def handle(self, *args, **options):
        for o in Language.objects.all().order_by('slug'):
            if len(o.family.all()) == 0:
                print o
