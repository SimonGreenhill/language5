from django.core.management.base import BaseCommand

from website.apps.statistics.models import statistic

class Command(BaseCommand):
    args = ''
    help = 'Displays all the defined statistics in the database'
    
    def handle(self, *args, **options):
        s = statistic.update(save=False)
        for label, value in s.items():
            print(f"{label.ljust(30)} {value}")
