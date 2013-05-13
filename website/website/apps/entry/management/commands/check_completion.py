# -*- coding: utf-8 -*-
import os
import codecs
from django.db import transaction
from django.core.management.base import BaseCommand

from website.apps.entry.models import Task
from website.apps.entry.views import decode_checkpoint, make_querydict
from website.apps.entry.dataentry.generic import GenericFormSet


class Command(BaseCommand):
    args = '<task_id>'
    help = 'Tests a task to see if it is complete'
    
    def display_task(self, task):
        print 
        print 'Name:'.ljust(15), task.name
        print 'Description:'.ljust(15), task.description
        print 'Source:'.ljust(15), task.source
        print 'Language:'.ljust(15), task.language
        print 'Records:'.ljust(15), task.records
        print 'View:'.ljust(15), task.view
        print 'Completable:'.ljust(15), task.completable
        print 'Done:'.ljust(15), task.done
        print
    
    def display_checkpoint(self, task):
        has_checkpoint = True if task.checkpoint not in (None, u"") else False
        
        print 'Checkpoint:'.ljust(15), has_checkpoint
        
        if not has_checkpoint:
            return
        
        try:
            print 'Checkpoint:'.ljust(15), task.checkpoint[0:64], '...'
        except:
            print 'Checkpoint:', repr(task.checkpoint)
        
        print
        print 'Checkpoint Decodes: '
        try:
            print decode_checkpoint(task.checkpoint)
        except:
            print '<error>'
        print
        print 'Checkpoint QueryDict: '
        try:
            cp = make_querydict(decode_checkpoint(task.checkpoint))
            print cp
        except:
            print '<error>'
        print
        
        return cp
        
    def display_formset(self, checkpoint):
        formset = GenericFormSet(checkpoint)
        print 'Formset:'.ljust(15), repr(formset)
        print 'is_valid:'.ljust(15), formset.is_valid()
        print
        
        for i, f in enumerate(formset.forms):
            print 'Form %d:'.ljust(15) % i, repr(f)
            print 'is_valid:'.ljust(15), f.is_valid()
            print 'errors:'.ljust(15), f.errors
            print
        
    def handle(self, *args, **options):
        task = Task.objects.select_related().get(pk=args[0])
        self.display_task(task)
        cp = self.display_checkpoint(task)
        if cp is None:
            return
        if 'submit' in cp:
            print 'Form:'.ljust(15), '<SUBMIT>'
        elif 'refresh' in cp:
            print 'Form:'.ljust(15), '<REFRESH>'
        else:
            print 'Form:'.ljust(15), '?'
        
        self.display_formset(cp)
            