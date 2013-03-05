from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

from website.apps.core.models import TrackedModel

class Task(TrackedModel):
    """Data Entry Tasks"""
    name = models.CharField(max_length=255, db_index=True,
        help_text="Name of Task")
    description = models.TextField(help_text="Task Description")
    view = models.CharField(default=entry_forms[0], max_length=256, 
            choices=entry_forms,
            help_text="Entry Forms")
    image = models.ImageField(upload_to='data/%Y-%m/',
        help_text="The Page Image")
    done = models.BooleanField(default=False, db_index=True,
        help_text="Data has been entered")
    
    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        return ('task-detail', [self.id])
    
    class Meta:
        db_table = 'tasks'

