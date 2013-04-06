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
    
    def save(self):
        if not self.pk:
            do_prefill = True
        else:
            do_prefill = False
        super(Paradigm, self).save(*args, **kwargs)
        
        if do_prefill:
            self._prefill_pronouns() # Prefill Pronouns
    
    def _prefill_pronouns(self):
        for p, n, g, a in Pronoun._generate_all_combinations():
            print p, n, g, a
    
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
        ('P', 'Possessive'),
    )
    
    PERSON_CHOICES = (
        ('1', '1st (excl) Person'),
        ('12', '1st (incl) Person'),
        ('2', '2nd Person'),
        ('3', '3rd Person'),
    )
    
    NUMBER_CHOICES = (
        ('sg', 'Singular'),
        ('du', 'Dual'),
        ('pl', 'Plural'),
       # ('tr', 'Trial'),
    )
    
    GENDER_CHOICES = (
        ("M", 'Masculine'),
        ("F", 'Feminine'),
      #  ("N", "Neuter"),
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
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,
        blank=True, null=True,
        help_text="Gender")
    form = models.TextField(blank=True, null=True,
        help_text="Form")
        
    def __unicode__(self):
        return '%s %s%s %s: %s' % (self.paradigm, self.person, self.number, self.alignment, self.gloss)
    
    @staticmethod
    def _generate_all_combinations():
        out = []
        for p in Pronoun.PERSON_CHOICES:
            for n in Pronoun.NUMBER_CHOICES:
                for g in Pronoun.GENDER_CHOICES:
                    for a in Pronoun.ALIGNMENT_CHOICES:
                        if p[0] == '12' and n[0] == 'sg':
                            continue
                        out.append((p[0], n[0], g[0], a[0]))
        return out
    
    @staticmethod
    def _generate_all_combinations_in_rows():
        out = {}
        for p in Pronoun.PERSON_CHOICES:
            out[p] = out.get(p, [])
            for n in Pronoun.NUMBER_CHOICES:
                for g in Pronoun.GENDER_CHOICES:
                    for a in Pronoun.ALIGNMENT_CHOICES:
                        if p[0] == '12' and n[0] == 'sg':
                            continue
                        out[p].append((p[0], n[0], g[0], a[0]))
        return out
        
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
        
        