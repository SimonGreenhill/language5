import os
from django.db import transaction
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    args = '<filename ../path/to/file>'
    help = 'Imports the given data file'
    
    @transaction.commit_manually
    def handle(self, *args, **options):
        for filename in args:
            filename = filename.strip()
            if not os.path.isfile(filename):
                raise IOError('Invalid Filename %s' % filename)
            
            filehead, fileext = os.path.splitext(filename)
            
            if fileext != '.py':
                raise IOError('Unable to import a %s file' % fileext)
            
            self.stdout.write('Beginning transaction...\n')
            
            try:
                self.stdout.write('Importing "%s"\n' % filename)
                execfile(filename)
            except:
                transaction.rollback()
                raise
            else:
                transaction.commit()
            
            self.stdout.write('Ending transaction...\n')


