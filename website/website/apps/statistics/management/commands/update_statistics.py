from django.core.management.base import BaseCommand

from website.apps.statistics.models import statistic

class Command(BaseCommand):
    args = ''
    help = 'Updates all the defined statistics in the database'

    def add_arguments(self, parser):
        parser.add_argument('args', nargs='*')
    
    def handle(self, *args, **options):
        statistic.update()
