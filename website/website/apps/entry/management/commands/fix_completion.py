# -*- coding: utf-8 -*-
import json
import codecs
from django.db import transaction
from django.core.management.base import BaseCommand

from website.apps.entry.models import Task
from website.apps.entry.views import decode_checkpoint, encode_checkpoint, make_querydict

class Command(BaseCommand):
    args = '<task_id>'
    help = 'Tests a task to see if it is complete'
    
    def _get(self, id, word):
        return u'form-%d-%s' % (id, word)
        
    def handle(self, *args, **options):
        task = Task.objects.select_related().get(pk=args[0])
        cp = make_querydict(decode_checkpoint(task.checkpoint))
        total_forms = int(cp['form-TOTAL_FORMS'])
        print 'Total Forms:', total_forms
        print 
        print 'OLD CHECKPOINT:'
        print json.dumps(cp, indent=4)
        print
        # TRY TO FIX:
        newcp = cp.copy()
        changes = 0
        
        for i in range(0, total_forms):
            for word in ('source', 'word', 'language', 'entry'):
                token = self._get(i, word)
                if word == 'language':
                    assert task.language, 'Task does not have a set language - failing'
                    value = cp.get(token, None)
                    expected = u'%d' % task.language.id
                    if value != expected:
                        newcp[token] = expected
                        print "Fixing language: %s - %r -> %r " % (token, value, expected)
                        changes += 1
                elif word == 'source':
                    assert task.source, 'Task does not have a set source - failing'
                    value = cp.get(token, None)
                    expected = u'%d' % task.source.id
                    if value != expected:
                        newcp[token] = expected
                        print "Fixing source: %s - %r -> %r " % (token, value, expected)
                        changes += 1
                    
                elif token not in cp and word in ('entry', 'word'):
                    print "Error - missing: %s - I can't fix this" % token
        
        if changes == 0:
            quit("No changes to make")
        else:
            print
            print 'NEW CHECKPOINT:'
            print json.dumps(newcp, indent=4)
            
            # save as file
            filename = 'task_%d_checkpoint.json' % task.id
            print 'Writing old checkpoint to %s' % filename
            with open(filename, 'w') as handle:
                handle.write(encode_checkpoint(cp))
            
            print 'Writing old checkpoint to task.checkpoint'
            task.checkpoint = encode_checkpoint(make_querydict(newcp))
            task.save()
        
        