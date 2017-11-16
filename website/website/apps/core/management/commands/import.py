# -*- coding: utf-8 -*-
import os
import re
import sys
from optparse import make_option
from django.conf import settings
from django.db import transaction
from django.core.management.base import BaseCommand

is_script = re.compile(r"""^[\d|x]{4}_.*\.py$""")

class Command(BaseCommand):
    args = '<filename ../path/to/file>'
    help = 'Imports the given data file'
    output_transaction = True
    
    DATA_ROOT = os.path.join(os.path.split(settings.SITE_ROOT)[0], 'data')
    
    def add_arguments(self, parser):
        parser.add_argument('filename', default=None, action='store')
        parser.add_argument('--run',
            action='store_true',
            dest='run',
            default=False,
            help='Run'
        )
    
    def list_datafiles(self):
        files = [_ for _ in os.listdir(self.DATA_ROOT)]
        files = [_ for _ in files if is_script.match(_)]
        for filename in sorted(files):
            print(" - {0}".format(os.path.join('data', filename)))
    
    def load(self, filename, dryrun=True):
        directory, module_name = os.path.split(filename)
        module_name = os.path.splitext(module_name)[0]
        sys.path.insert(0, directory)
        
        with transaction.atomic():
            __import__(module_name)
            if dryrun:
                raise ValueError("No save -- Rollback") 
            else:
                print("\n<<< COMMIT\n")
    
    def handle(self, *args, **options):
        # set some environment variables;
        os.environ['IMPORTER_SITEROOT'] = settings.SITE_ROOT
        os.environ['IMPORTER_DATAROOT'] = self.DATA_ROOT
        
        # handle no args
        if options['filename'] is None:
            print("Listing files in {0}:".format(self.DATA_ROOT))
            self.list_datafiles()
            return
        
        # set some environment variables;
        os.environ['IMPORTER_FILENAME'] = options['filename']
        options['filename'] = options['filename'].strip()
        if not os.path.isfile(options['filename']):
            raise IOError('Invalid Filename %s' % options['filename'])
        
        filehead, fileext = os.path.splitext(options['filename'])
        
        if fileext != '.py':
            raise IOError('Unable to import a %s file' % fileext)
        
        self.stdout.write('Importing "%s"\n' % options['filename'])
        
        if 'run' in options and options['run']:
            self.load(options['filename'], dryrun=False)
        else:
            self.load(options['filename'], dryrun=True)
            sys.stdout.write(
                "Dry-run complete. Use --run to save changes. Rolling back."
            )
        self.stdout.flush()
            
