from django.db import models
from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from django.urls import reverse
from website.signals import create_redirect

from reversion import revisions as reversion
from watson import search as watson

from website.apps.statistics.models import statistic

# The AllMethodCachingQueryset and AllMethodCachingManager add cached querysets for 
# use in formsets. This makes life much easier for the poor database. Have hooked
# them into TrackedModel to enable them everywhere.
# see: http://stackoverflow.com/questions/8176200/caching-queryset-choices-for-modelchoicefield-or-modelmultiplechoicefield-in-a-d
class AllMethodCachingQueryset(models.query.QuerySet):
    def all(self, get_from_cache=True):
        if get_from_cache:
            return self
        else:
            return self._clone()


class AllMethodCachingManager(models.Manager):
    def get_queryset(self):
        return AllMethodCachingQueryset(self.model, using=self._db)


class TrackedModel(models.Model):
    """Abstract base class containing editorial information"""
    editor = models.ForeignKey(User, on_delete=models.PROTECT)
    added = models.DateTimeField(auto_now_add=True)
    
    objects = models.Manager()
    cache_all_method = AllMethodCachingManager()
    
    class Meta:
        abstract = True
        get_latest_by = 'added'


@reversion.register
class Source(TrackedModel):
    """Source Details"""
    year = models.CharField(max_length=12, 
        blank=True, null=True, db_index=True,
        help_text="Year published")
    author = models.CharField(max_length=255, db_index=True, 
        help_text="Short Author list e.g. (Smith et al.)")
    slug = models.SlugField(max_length=64, unique=True,
        help_text="`Slug` for author i.e. author-year (for use in URLS)")
    reference = models.TextField(blank=True, null=True,
        help_text="Reference for Source")
    bibtex = models.TextField(blank=True, null=True,
        help_text="BibTeX entry")
    comment = models.TextField(blank=True, null=True,
        help_text="Private comment on source")
    
    def __str__(self):
        if self.year is not None:
            return f"{self.author} ({self.year})"
        else:
            return str(self.author)
    
    def get_absolute_url(self):
        return reverse('source-detail', kwargs={'slug': self.slug})
    
    class Meta:
        db_table = 'sources'
        ordering = ['author', 'year', ]
        indexes = [models.Index(fields=["author", "year"])]


@reversion.register
class Note(TrackedModel):
    """Notes/Information about a language"""
    language = models.ForeignKey('Language', on_delete=models.CASCADE)
    source = models.ForeignKey('Source', on_delete=models.CASCADE)
    note = models.TextField(help_text="Note")
    location = models.CharField(max_length=50, blank=True, null=True,
        help_text="Location (e.g. p12)")
    
    class Meta:
        db_table = 'notes'


@reversion.register
class Family(TrackedModel):
    """Language families/Subsets"""
    family = models.CharField(max_length=64, unique=True, db_index=True, 
        help_text="Language Family")
    slug = models.SlugField(max_length=64, unique=True,
        help_text="`Slug` for language family (for use in URLS)")
    
    def __str__(self):
        return str(self.family)
        
    def get_absolute_url(self):
        return reverse('family-detail', kwargs={'slug': self.slug})
    
    class Meta:
        db_table = 'families'
        verbose_name_plural = 'families'
        ordering = ['family', ]
    

@reversion.register
class Language(TrackedModel):
    """Stores language information"""
    family = models.ManyToManyField(Family, blank=True)
    language = models.CharField(max_length=64, db_index=True,
        help_text="Language Name")
    dialect = models.CharField(max_length=64, db_index=True, null=True, blank=True,
        help_text="Dialect")
    slug = models.SlugField(max_length=64, unique=True,
        help_text="`Slug` for language (for use in URLS)")
    isocode = models.CharField(max_length=3, blank=True, null=True, db_index=True,
        help_text="3 character ISO-639-3 Code.")
    glottocode = models.CharField(max_length=8, blank=True, null=True, db_index=True,
        help_text="Glottolog Code.")
    classification = models.TextField(blank=True, null=True,
        help_text="Classification String")
    information = models.TextField(blank=True, null=True,
        help_text="Information about language")
    
    def __str__(self):
        if self.dialect:
            return f"{self.language} ({self.dialect} Dialect)"
        else:
            return str(self.language)
    
    def get_absolute_url(self):
        return reverse('language-detail', kwargs={'language': self.slug})
    
    class Meta:
        unique_together = ("isocode", "language", "dialect")
        indexes = [models.Index(fields=["language", "dialect"])]
        db_table = 'languages'
        ordering = ['language', 'dialect']


@reversion.register
class AlternateName(TrackedModel):
    """Handles languages with multiple names"""
    language = models.ForeignKey('Language', on_delete=models.CASCADE)
    name = models.CharField(max_length=64, unique=True, db_index=True,
        help_text="Alternate Name for this language")
    slug = models.SlugField(max_length=64, unique=True,
        help_text="`Slug` for language (for use in URLS)")
    
    def __str__(self):
        return str(f"{self.language} AKA {self.slug}")
        
    def get_absolute_url(self):
        return reverse('language-detail', kwargs={'language': self.language.slug})
        
    class Meta:
        verbose_name_plural = 'Alternate Language Names'
        db_table = 'altnames'
        ordering = ['name', ]


@reversion.register
class Link(TrackedModel):
    """Stores links to language appropriate resources"""
    language = models.ForeignKey('Language', on_delete=models.CASCADE)
    link = models.URLField(help_text="URL to link")
    description = models.TextField(help_text="Language Description")
    
    def __str__(self):
        return str("%d %s" % (self.language.id, self.link))
    
    class Meta:
        verbose_name_plural = "Resource Links"
        db_table = 'links'
        unique_together = ['language', 'link']
        

@reversion.register
class Location(TrackedModel):
    isocode = models.CharField(max_length=3, db_index=True)
    longitude = models.FloatField(help_text="Longitude")
    latitude = models.FloatField(help_text="Latitiude")

    class Meta:
        verbose_name_plural = "Geographical Locations"
        db_table = 'locations'


@reversion.register
class Attachment(TrackedModel):
    """Attachments Details"""
    language = models.ForeignKey('Language', on_delete=models.CASCADE)
    source = models.ForeignKey('Source', on_delete=models.CASCADE)
    details = models.CharField(max_length=32, null=True, blank=True,
        help_text="Extra details e.g. page number")
    file = models.FileField(upload_to='data/%Y-%m/',
        help_text="The Resource File (PDF)", null=True, blank=True)
        
    def __str__(self):
        return str(self.file.name)
    
    def get_absolute_url(self):
        return self.file.url
        
    class Meta:
        db_table = 'attachments'


# pre-save adding of redirects when slug field altered.
pre_save.connect(create_redirect, sender=Source, dispatch_uid="source:001")
pre_save.connect(create_redirect, sender=Family, dispatch_uid="family:001")
pre_save.connect(create_redirect, sender=Language, dispatch_uid="language:001")


watson.register(Language, 
    fields=('family', 'language', 'dialect', 'isocode', 'classification', 'information')
)
watson.register(Family, fields=('family',))
watson.register(Source, fields=('author', 'year', 'reference'))
watson.register(AlternateName, fields=('language', 'name'))
watson.register(Link, fields=('language', 'link', 'description'))

statistic.register("Number of Families", Family)
statistic.register("Number of Languages", Language, graph=1)
statistic.register("Number of Sources", Source, graph=2)
statistic.register("Number of Notes", Note)
statistic.register("Number of Alternate Names", AlternateName)
statistic.register("Number of Locations", Location)
statistic.register("Number of Links", Link)
statistic.register("Number of Files", Attachment)

