from django.db import models
from django.core.urlresolvers import reverse

from website.apps.core.models import TrackedModel, Language, Source


class Paradigm(TrackedModel):
    """Paradigm Details"""
    language = models.ForeignKey(Language)
    source = models.ForeignKey(Source)
    comment = models.TextField(blank=True, null=True,
        help_text="Comment on this paradigm")
    
    def __unicode__(self):
        return "Paradigm: %s" % self.language.slug
    
    @models.permalink
    def get_absolute_url(self):
        return ('pronoun:edit', [self.slug])
    
    class Meta:
        db_table = 'paradigms'
        

class Pronoun(TrackedModel):
    """Pronoun Data"""
    ALIGNMENT_CHOICES = (
        ('A', 'A'),
        ('S', 'S'),
        ('O', 'O'),
        ('P', 'P'),
    )
    
    PERSON_CHOICES = (
        ('1', '1st Person'),
        ('2', '2nd Person'),
        ('3', '3rd Person'),
        ('12', '12 Person'),
    )
    
    NUMBER_CHOICES = (
        ('sg', 'Singular'),
        ('du', 'Dual'),
        ('pl', 'Plural'),
        ('tr', 'Trial'),
    )
    
    paradigm = models.ForeignKey('Paradigm')
    comment = models.TextField(blank=True, null=True,
        help_text="Comment on this paradigm")
    alignment = models.CharField(max_length=1, choices=ALIGNMENT_CHOICES,
        help_text="Alignment")
    person = models.CharField(max_length=2, choices=PERSON_CHOICES,
        help_text="Person")
    number = models.CharField(max_length=2, choices=NUMBER_CHOICES,
        help_text="Number")
    gloss = models.TextField(blank=True, null=True,
        help_text="Gloss")
        
    def __unicode__(self):
        return '%s %s%s %s: %s' % (self.paradigm, self.person, self.number, self.alignment, self.gloss)
        
    class Meta:
        db_table = 'pronouns'
        
        
class Relationship(TrackedModel):
    """Relationships Data"""
    RELATIONSHIP_CHOICES = (
        ('TD', 'Totally Distinct'),
        ('FO', 'Formal Overlap'),
        ('FI', 'Formal Increment'),
        ('TS', 'Total Syncretism'),
    )
    
    paradigm = models.ForeignKey('Paradigm')
    pronoun1 = models.ForeignKey('Pronoun', related_name="pronoun1")
    pronoun2 = models.ForeignKey('Pronoun', related_name="pronoun2")
    relationship = models.CharField(max_length=2, choices=RELATIONSHIP_CHOICES,
        default=None, blank=True, null=True, help_text="Relationship")
    comment = models.TextField(blank=True, null=True,
        help_text="Comment on this paradigm")
    
    def __unicode__(self):
        return '<Relationship: %d-%d>' % (self.pronoun1, self.pronoun2)

    class Meta:
        db_table = 'pronoun_relationships'
        
        