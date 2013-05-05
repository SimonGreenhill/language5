from django.db import models
from django.contrib.auth.models import User
from website.apps.core.models import TrackedModel
from website.apps.entry.dataentry import available_views
from website.apps.statistics import statistic


class TaskLog(models.Model):
    """Task Log"""
    person = models.ForeignKey(User)
    page = models.CharField(max_length=64)
    message = models.CharField(max_length=255)
    time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'tasklog'
        

class Task(TrackedModel):
    """Data Entry Tasks"""
    name = models.CharField(max_length=255, db_index=True,
        help_text="Name of Task")
    description = models.TextField(help_text="Task Description")
    source = models.ForeignKey('core.Source')
    language = models.ForeignKey('core.Language', blank=True, null=True)
    records = models.IntegerField(blank=True, null=True, default=20)
    view = models.CharField(default=available_views[0][0], max_length=256,
            choices=available_views,
            help_text="Data entry view to Use")
    image = models.ImageField(upload_to='data/%Y-%m/',
        help_text="The Page Image", null=True, blank=True)
    file = models.FileField(upload_to='data/%Y-%m/',
        help_text="The Resource File (PDF)", null=True, blank=True)
    completable = models.BooleanField(default=True, db_index=True,
        help_text="Is task completable or not?")
    done = models.BooleanField(default=False, db_index=True,
        help_text="Data has been entered")
    checkpoint = models.TextField(help_text="Saved Checkpoint Data", 
        blank=True, null=True)
    
    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        return ('entry:detail', [self.id])
    
    class Meta:
        db_table = 'tasks'


statistic.register("Number of Data Entry Tasks", Task)
