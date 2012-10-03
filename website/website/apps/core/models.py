from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class TrackedModel(models.Model):
    """Abstract base class containing editorial information"""
    editor = models.ForeignKey(User)
    added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True


class Family(TrackedModel):
    """Language families/Subsets"""
    family = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=64, unique=True)
    
    def __unicode__(self):
        return self.family
    
    def get_absolute_url(self):
        return reverse('core.views.family_detail', args=[self.slug])
    
    class Meta:
        db_table = 'families'
    
    

class Language(TrackedModel):
    """Stores language information"""
    language = models.CharField(max_length=64, unique=True, db_index=True)
    slug = models.SlugField(max_length=64, unique=True, db_index=True)
    isocode = models.CharField(max_length=3, blank=True, db_index=True)
    classification = models.TextField(blank=True)
    information = models.TextField(blank=True)
    
    family = models.ManyToManyField(Family, blank=True)
    
    def __unicode__(self):
        return self.language
    
    def get_absolute_url(self):
        return reverse('website.apps.core.views.language_detail', args=[self.slug])
        
    class Meta:
        unique_together = ("isocode", "language")
        db_table = 'languages'


class AlternateNames(TrackedModel):
    """Handles languages with multiple names"""
    language = models.ForeignKey(Language)
    
    name = models.CharField(max_length=64, unique=True, db_index=True)
    slug = models.SlugField(max_length=64, unique=True, db_index=True)
    
    def __unicode__(self):
        return "%d AKA %s" % (self.language.id, self.slug)
        
    class Meta:
        verbose_name_plural = 'Alternate Language Names'
        db_table = 'altnames'


class Links(TrackedModel):
    """Stores links to language appropriate resources"""
    language = models.ForeignKey(Language)
    
    link = models.URLField()
    description = models.TextField()
    
    def __unicode__(self):
        return "%d %s" % (self.language.id, self.link)

    class Meta:
        verbose_name_plural = "Resource Links"
        db_table = 'links'


class Locations(TrackedModel):
    language = models.ForeignKey(Language)

    longitude = models.FloatField()
    latitude = models.FloatField()

    def __unicode__(self):
        return "%d %2.4f-%2.4f" % (self.language.id, self.longitude, self.latitude)

    class Meta:
        verbose_name_plural = "Geographical Locations"
        db_table = 'locations'

