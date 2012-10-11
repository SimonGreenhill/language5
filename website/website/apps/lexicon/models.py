from django.db import models
from django.core.urlresolvers import reverse

from website.apps.core.models import TrackedModel



COGNATE_QUALITY = (
    (0, 'Unassessed'),
    (1, 'Published'),
    (2, 'Accepted'),
    # space for more..
    (9, 'Problematic'),
)



class Word(TrackedModel):
    """Word Details"""
    word = models.CharField(max_length=64, db_index=True,
        help_text="Word in English")
    slug = models.SlugField(max_length=64, unique=True,
        help_text="`Slug` for word i.e. author-year (for use in URLS)")
    full = models.TextField(blank=True, null=True,
        help_text="Full word details/gloss.")
    
    def __unicode__(self):
        return self.slug
        
    def get_absolute_url(self):
        return reverse('website.apps.lexicon.views.word_detail', args=[self.slug])
    
    class Meta:
        db_table = 'words'


class WordSubset(TrackedModel):
    """Word Subset Details"""
    subset = models.CharField(max_length=64, db_index=True,
        help_text="Subset Label")
    slug = models.SlugField(max_length=64, unique=True,
        help_text="`Slug` for subset i.e. author-year (for use in URLS)")
    description = models.TextField(blank=True, null=True,
        help_text="Details of subset.")
    words = models.ManyToManyField('Word', blank=True, null=True)
    
    def __unicode__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('website.apps.lexicon.views.subset_detail', args=[self.slug])
    

    class Meta:
        db_table = 'wordsubsets'


class Lexicon(TrackedModel):
    """Lexicon Details"""
    language = models.ForeignKey('core.Language')
    source = models.ForeignKey('core.Source')
    word = models.ForeignKey('Word')
    
    entry = models.CharField(max_length=32, 
        help_text="Entry from source")
    phon_entry = models.CharField(max_length=32, null=True, blank=True,
        help_text="Entry in Phonological format (in known)")
    
    annotation = models.TextField(blank=True, null=True,
        help_text="Annotation for this item")
    
    loan = models.BooleanField(default=False, db_index=True,
        help_text="Is a loan word?")
    loan_source = models.ForeignKey('core.Language', blank=True, null=True, 
        related_name = 'loan_source_set',
        help_text="Loanword Source (if known)"
    )
    
    def __unicode__(self):
        return u"%d-%s" % (self.id, self.entry)

    class Meta:
        db_table = 'lexicon'



class Cognate(TrackedModel):
    """Cognacy Judgements"""
    lexeme = models.ManyToManyField('Lexicon')
    source = models.ForeignKey('core.Source', 
        null=True, blank=True)
    comment = models.TextField(blank=True, null=True,
        help_text="Comment about this Cognate set")
    quality = models.CharField(default=0, max_length=1, choices=COGNATE_QUALITY,
            help_text="The quality of this cognate set.")
    
    def get_absolute_url(self):
        return reverse('website.apps.lexicon.views.cognate_detail', args=[self.id])
    
    
    def __unicode__(self):
        return self.id
    
    class Meta:
        db_table = 'cognates'



class Correspondence(TrackedModel):
    """Sound Correspondence Sets"""
    language = models.ManyToManyField('core.Language', through='Rule')
    source = models.ForeignKey('core.Source', blank=True, null=True)
    comment = models.TextField(blank=True, null=True, help_text="Notes")
    
    class Meta:
        db_table = 'correspondences'


class Rule(TrackedModel):
    """Sound Correspondence Rules"""
    language = models.ForeignKey('core.Language')
    group = models.ForeignKey(Correspondence)
    rule = models.CharField(max_length=5)
    
    class Meta:
        db_table = 'corrrules'
