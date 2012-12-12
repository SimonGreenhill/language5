from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

from website.apps.core.models import TrackedModel

class Task(TrackedModel):
    """Data Entry Tasks"""
    name = models.CharField(max_length=255,
        help_text="Name of Task")
    formname = models.CharField(max_length=255,
        help_text="Name of Form")
    
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
    comment = models.TextField(help_text="Comments")
    description = models.CharField(max_length=64,
        help_text="Short description (e.g. page numbers)")
    image = models.ImageField(upload_to='data/%Y-%m/',
        help_text="The Page Image")
    done = models.BooleanField(default=False, db_index=True,
        help_text="Data has been entered")
    
    def __unicode__(self):
        return u'#%d. %s' % (self.task_id, self.description)
        
    def get_absolute_url(self):
        return ('task-entry', [self.id])
    
    class Meta:
        db_table = 'entry_contents'


class Result(TrackedModel):
    task = models.ForeignKey('Task')
    content = models.ForeignKey('Content')
    result = models.TextField(
        help_text="Raw JSON content")
    comment = models.TextField(help_text="Comments")
    imported = models.BooleanField(default=False, db_index=True,
        help_text="Imported into main database or not")
        
    def __unicode__(self):
        return u'#Task %d. Subset %d' % (self.task_id, self.content_id)

    class Meta:
        db_table = 'entry_results'
    