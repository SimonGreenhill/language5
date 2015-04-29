# -*- coding: utf-8 -*-
from django.db import transaction
from django.core.management.base import BaseCommand

from website.apps.statistics import statistic
from website.apps.statistics.models import StatisticalValue

class Command(BaseCommand):
    args = ''
    help = 'Displays all the defined statistics in the database'
    
    def handle(self, *args, **options):
        statistic.update(save=True)
        for v in StatisticalValue.objects.all().order_by('-date'):
            date = v.date.isoformat().split("T")[0]
            print("\t".join([v.label, date, '%d' % v.value]))
