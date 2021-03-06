from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.utils import six
from website.apps.core.models import TrackedModel
from website.apps.entry.dataentry import available_views
from website.apps.statistics.models import statistic


@python_2_unicode_compatible
class Task(TrackedModel):
    """Data Entry Tasks"""
    name = models.CharField(max_length=255, db_index=True,
        help_text="Name of Task")
    description = models.TextField(help_text="Task Description", blank=True, null=True)
    source = models.ForeignKey('core.Source', blank=True, null=True)
    wordlist = models.ForeignKey('Wordlist', blank=True, null=True)
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
    lexicon = models.ManyToManyField('lexicon.Lexicon',
        help_text="Saved Lexical Items", blank=True)
    
    def __str__(self):
        return six.text_type(self.name)
    
    @models.permalink
    def get_absolute_url(self):
        return ('entry:detail', [self.id])
    
    def save(self, *args, **kwargs):
        # over-ride records with length of wordlist.
        if self.wordlist:
            self.records = self.wordlist.words.count()
        super(Task, self).save(*args, **kwargs)

    class Meta:
        db_table = 'tasks'
        ordering = ['name', ]
        get_latest_by = 'date'


class TaskLog(models.Model):
    """Task Log"""
    person = models.ForeignKey(User)
    task = models.ForeignKey(Task, blank=True, null=True, db_index=True)
    page = models.CharField(max_length=64)
    message = models.CharField(max_length=255)
    time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'tasklog'
        ordering = ['time', ]
        get_latest_by = 'time'


@python_2_unicode_compatible
class Wordlist(TrackedModel):
    """Wordlist for data entry tasks"""
    name = models.CharField(max_length=255, db_index=True, unique=True,
        help_text="Name of Wordlist")
    words = models.ManyToManyField('lexicon.Word', through="WordlistMember")
    
    def __str__(self):
        return six.text_type(self.name)
    
    class Meta:
        db_table = 'task_wordlists'
        ordering = ['name', ]
    

class WordlistMember(models.Model):
    wordlist = models.ForeignKey("entry.Wordlist")
    word = models.ForeignKey("lexicon.Word")
    order = models.IntegerField(db_index=True)
    
    class Meta:
        ordering = ["order", ]
        db_table = 'task_wordlists_members'


statistic.register("Number of Data Entry Tasks", Task)
