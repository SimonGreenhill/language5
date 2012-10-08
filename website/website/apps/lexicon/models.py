from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from website.apps.core.models import TrackedModel, Source, Language

COGNATE_QUALITY = (
    (0, 'Unassessed'),
    (1, 'Published'),
    (2, 'Accepted'),
    # space for more..
    (9, 'Problematic'),
)




class Word(TrackedModel):
    """Word Details"""
    word = models.CharField(max_length=64,
        help_text="Word in English")
    slug = models.SlugField(max_length=64, unique=True, db_index=True,
        help_text="`Slug` for word i.e. author-year (for use in URLS)")
    full = models.TextField(blank=True, null=True,
        help_text="Full word details/gloss.")
    
    def __unicode__(self):
        return self.slug
        
    # def get_absolute_url(self):
    #     return reverse('website.apps.core.views.source_detail', args=[self.slug])
    # 
    
    class Meta:
        db_table = 'words'


class WordSubset(TrackedModel):
    """Word Subset Details"""
    subset = models.CharField(max_length=64,
        help_text="Subset Label")
    slug = models.SlugField(max_length=64, unique=True, db_index=True,
        help_text="`Slug` for subset i.e. author-year (for use in URLS)")
    description = models.TextField(blank=True, null=True,
        help_text="Details of subset.")
    words = models.ManyToManyField('Word', blank=True, null=True)
    
    def __unicode__(self):
        return self.slug

    # def get_absolute_url(self):
    #     return reverse('website.apps.core.views.source_detail', args=[self.slug])
    # 

    class Meta:
        db_table = 'wordsubset'


class Lexeme(TrackedModel):
    """Lexicon Details"""
    language = models.ForeignKey(Language)
    word = models.ForeignKey('Word')
    source = models.ForeignKey(Source)
    ### ENTRY
    annotation = models.TextField(blank=True, null=True,
        help_text="Annotation for this item")

    def __unicode__(self):
        return self.slug

    class Meta:
        db_table = 'lexeme'


class Cognate(TrackedModel):
    """Cognacy Judgements"""
    lexeme = models.ManyToManyField('Lexeme')
    source = models.ForeignKey(Source, null=True, blank=True)
    comment = models.TextField(blank=True, null=True,
        help_text="Comment about this Cognate set")
    quality = models.CharField(default=0, max_length=1, choices=COGNATE_QUALITY,
            help_text="The quality of this cognate set.")
    
    # def get_absolute_url(self):
    #     return reverse('website.apps.core.views.source_detail', args=[self.slug])
    # 
    
    def __unicode__(self):
        return self.id
    
    class Meta:
        db_table = 'cognate'
    