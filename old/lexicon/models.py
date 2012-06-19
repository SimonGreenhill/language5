from django.db import models
from django.contrib.auth.models import User

from languages.models import Language, TrackedModel
from sources.models import Source

class Word(TrackedModel):
    """Stores Words"""
    word = models.CharField(max_length=32)
    slug = models.SlugField(max_length=32)
    extra = models.CharField(max_length=255)
    
    def __unicode__(self):
        return "<%d %s>" % (self.id, self.slug)

    def get_absolute_url(self):
        return "/words/%s/" % self.slug

    class Meta:
        db_table = 'words'


class Entries(TrackedModel):
    """Lexical Items"""
    language = models.ForeignKey(Language)
    word = models.ForeignKey(Word)
    source = models.ForeignKey(Source)
    
    entry = models.TextField()
    annotation = models.TextField()
    
    enteredby = models.CharField(max_length=32)
    
    cognacy = models.CharField(max_length=20)
    
    is_current = models.BooleanField()
    
    def __unicode__(self):
        return "<%d-%d-%d>" % (self.language.id, self.word.id, self.id)


class Categories(models.Model):
    """Word Categories"""
    category = models.CharField(max_length=32)
    slug = models.SlugField(max_length=32)
    
    word = models.ManyToManyField(Word)
    
    def __unicode__(self):
        return "<%d %s>" % (self.id, self.slug)
    
    def get_absolute_url(self):
        return "/categories/%s/" % self.slug
    