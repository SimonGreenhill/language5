from django.db import models
from django.db.models.signals import pre_save
from django.core.urlresolvers import reverse

import watson

from website.apps.core.models import TrackedModel
from website.apps.statistics import statistic
from website.signals import create_redirect



COGNATESET_QUALITY = (
    ('0', 'Unassessed'),
    ('1', 'Published'),
    ('2', 'Accepted'),
    # space for more..
    ('9', 'Problematic'),
)

COGNATE_QUALITY = (
    ('0', 'Unassessed'),
    ('1', 'Published'),
    ('2', 'Accepted'),
    # space for more..
    ('9', 'Problematic'),
)

WORD_QUALITY = (
    ('0', 'Unassessed'),
    ('1', 'Extremely stable or reliable'),
    ('8', 'Open to serious objections as a test item'),
    ('9', 'Highly unsuitable'),
)

class Word(TrackedModel):
    """Word Details"""
    word = models.CharField(max_length=64, db_index=True, unique=True,
        help_text="Word in English")
    slug = models.SlugField(max_length=64, unique=True,
        help_text="`Slug` for word (for use in URLS)")
    full = models.TextField(blank=True, null=True,
        help_text="Full word details/gloss.")
    comment = models.TextField(blank=True, null=True,
        help_text="PUBLIC comment on this word")
    quality = models.CharField(default=u'0', max_length=1, choices=WORD_QUALITY,
            help_text="The quality of this word.")
    
    def __unicode__(self):
        if self.full:
            return u"%s (%s)" % (self.word, self.full)
        else:
            return self.word
    
    @property
    def fullword(self): 
        return self.__unicode__()
    
    @models.permalink
    def get_absolute_url(self):
        return ('word-detail', [self.slug])
    
    class Meta:
        db_table = 'words'
        ordering = ['word', ]




class WordSubset(TrackedModel):
    """Word Subset Details"""
    subset = models.CharField(max_length=64, db_index=True, unique=True, 
        help_text="Subset Label")
    slug = models.SlugField(max_length=64, unique=True,
        help_text="`Slug` for subset (for use in URLS)")
    description = models.TextField(blank=True, null=True,
        help_text="Details of subset.")
    words = models.ManyToManyField('Word', blank=True, null=True)
    
    def __unicode__(self):
        return self.slug
        
    @models.permalink
    def get_absolute_url(self):
        return ('subset-detail', [self.slug])
        
    class Meta:
        db_table = 'wordsubsets'
        verbose_name_plural = 'Word Subsets'
        ordering = ['slug', ]


class Lexicon(TrackedModel):
    """Lexicon Details"""
    language = models.ForeignKey('core.Language')
    source = models.ForeignKey('core.Source')
    word = models.ForeignKey('Word')
    
    entry = models.CharField(max_length=32, db_index=True, 
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
        verbose_name_plural = 'Lexical Items'
        ordering = ['entry', ]


class CognateSet(TrackedModel):
    """Cognate Sets"""
    protoform = models.CharField(max_length=128, blank=True, null=True, db_index=True)
    gloss = models.CharField(max_length=128, blank=True, null=True)
    comment = models.TextField(blank=True, null=True,
        help_text="Comment about this cognate set")
    source = models.ForeignKey('core.Source', 
        null=True, blank=True)
    lexicon = models.ManyToManyField('Lexicon', through='Cognate')
    quality = models.CharField(default=u'0', max_length=1, choices=COGNATESET_QUALITY,
            help_text="The quality of this cognate set.")
    
    def __unicode__(self):
        return "%d. %s '%s'" % (self.id, self.protoform, self.gloss)
    
    class Meta:
        db_table = 'cognatesets'
        verbose_name_plural = 'Cognate Sets'
    

class Cognate(TrackedModel):
    """Cognacy Judgements"""
    lexicon = models.ForeignKey('Lexicon')
    cognateset = models.ForeignKey('CognateSet')
    source = models.ForeignKey('core.Source', 
        null=True, blank=True)
    comment = models.TextField(blank=True, null=True,
        help_text="Comment about this Cognate set")
    flag = models.CharField(default=0, max_length=1, choices=COGNATE_QUALITY,
            help_text="The quality of this cognate.")
    
    def __unicode__(self):
        return u"%d.%d" % (self.cognateset_id, self.id)
    
    class Meta:
        db_table = 'cognates'


class CorrespondenceSet(TrackedModel):
    """Sound Correspondence Sets"""
    language = models.ManyToManyField('core.Language', through='Correspondence')
    source = models.ForeignKey('core.Source', blank=True, null=True)
    comment = models.TextField(blank=True, null=True, help_text="Notes")
    
    class Meta:
        db_table = 'corrsets'
        verbose_name_plural = 'Correspondence Sets'
        

class Correspondence(TrackedModel):
    """Sound Correspondence Rules"""
    language = models.ForeignKey('core.Language')
    corrset = models.ForeignKey('CorrespondenceSet')
    rule = models.CharField(max_length=5)
    
    class Meta:
        db_table = 'correspondences'


# pre-save adding of redirects when slug field altered.
pre_save.connect(create_redirect, sender=Word, dispatch_uid="word:001")
pre_save.connect(create_redirect, sender=WordSubset, dispatch_uid="wordsubset:001")


watson.register(Word, fields=('word', 'full'))
watson.register(WordSubset, fields=('subset', 'description'))
watson.register(Lexicon, fields=('entry', 'annotation'))


statistic.register("Number of Words", Word)
statistic.register("Number of Word Sets", WordSubset)
statistic.register("Number of Lexical Items", Lexicon)
statistic.register("Number of Cognates", Cognate)
statistic.register("Number of Cognate Sets", CognateSet)
statistic.register("Number of Correspondences", Correspondence)
statistic.register("Number of Correspondence Sets", CorrespondenceSet)
