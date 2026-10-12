import os
import sys
from django.conf import settings
from django.core.management.base import BaseCommand
from website.apps.lexicon.models import Word

sys.path.append(
    os.path.join(os.path.split(settings.SITE_ROOT)[0], 'data')
)
from synonyms import SYNONYMS

class Command(BaseCommand):
    args = ''
    help = 'Checks the synonym list'
    output_transaction = True

    def add_arguments(self, parser):
        parser.add_argument('args', nargs='*')
    
    def handle(self, *args, **options):
        for syn, slug in SYNONYMS.items():
            try:
                Word.objects.get(slug=slug)
            except Word.DoesNotExist:
                print(
                    f"Error: '{slug}' does not exist for synonym '{syn}'"
                )
