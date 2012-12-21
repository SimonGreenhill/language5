from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

from website.apps.core.models import TrackedModel

from website.apps.entry.forms import entry_forms

class Task(TrackedModel):
    """Data Entry Tasks"""
    name = models.CharField(max_length=255, db_index=True,
        help_text="Name of Task")
    comment = models.TextField(help_text="Comment")
    source = models.ForeignKey('core.Source', default=None, blank=True, null=True)
    form = models.CharField(default=entry_forms[0], max_length=256, 
            choices=entry_forms,
            help_text="Entry Forms")
    
    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        return ('task-detail', [self.id])
    
    class Meta:
        db_table = 'entry_tasks'


class Content(TrackedModel):
    """Task Content"""
    task = models.ForeignKey('Task')
    taskcomment = models.TextField(blank=True, null=True,
        help_text="Task Comment for Data Entry Person")
    comment = models.TextField(blank=True, null=True, 
        help_text="Comments from Data Entry Person")
    description = models.CharField(max_length=64,
        help_text="Short description (e.g. page numbers)")
    image = models.ImageField(upload_to='data/%Y-%m/',
        help_text="The Page Image")
    # raw result data
    result = models.TextField(default=None, blank=True, null=True,
        help_text="Raw JSON content")
    done = models.BooleanField(default=False, db_index=True,
        help_text="Data has been entered")
    imported = models.BooleanField(default=False, db_index=True,
        help_text="Imported into main database or not")
    
    def __unicode__(self):
        return u'#%d. %s' % (self.task_id, self.description)
        
    def get_absolute_url(self):
        return ('task-entry', [self.id])
    
    class Meta:
        db_table = 'entry_contents'

