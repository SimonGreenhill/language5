from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from website.apps.core.models import TrackedModel, Language, Source

PronounCombinations = [
    # 1st (excl) Person, Sing.
    {
        'alignment': ('A', 'A'),
        'gender': None,
        'number': ('sg', 'Singular'),
        'person': ('1', '1st (excl) Person')
    },
    {
        'alignment': ('S', 'S'),
        'gender': None,
        'number': ('sg', 'Singular'),
        'person': ('1', '1st (excl) Person')
    },
    {
        'alignment': ('O', 'O'),
        'gender': None,
        'number': ('sg', 'Singular'),
        'person': ('1', '1st (excl) Person')
    },
    {
        'alignment': ('P', 'Possessive'),
        'gender': None,
        'number': ('sg', 'Singular'),
        'person': ('1', '1st (excl) Person')
    },
    # 1st (excl) Person, Dual.
    {
        'alignment': ('A', 'A'),
        'gender': None,
        'number': ('du', 'Dual'),
        'person': ('1', '1st (excl) Person')
    },
    {
        'alignment': ('S', 'S'),
        'gender': None,
        'number': ('du', 'Dual'),
        'person': ('1', '1st (excl) Person')
    },
    {
        'alignment': ('O', 'O'),
        'gender': None,
        'number': ('du', 'Dual'),
        'person': ('1', '1st (excl) Person')
    },
    {
        'alignment': ('P', 'Possessive'),
        'gender': None,
        'number': ('du', 'Dual'),
        'person': ('1', '1st (excl) Person')
    },
    
    # 1st (excl) Person, Plural
    {
        'alignment': ('A', 'A'),
        'gender': None,
        'number': ('pl', 'Plural'),
        'person': ('1', '1st (excl) Person')
    },
    {
        'alignment': ('S', 'S'),
        'gender': None,
        'number': ('pl', 'Plural'),
        'person': ('1', '1st (excl) Person')
    },
    {
        'alignment': ('O', 'O'),
        'gender': None,
        'number': ('pl', 'Plural'),
        'person': ('1', '1st (excl) Person')
    },
    {
        'alignment': ('P', 'Possessive'),
        'gender': None,
        'number': ('pl', 'Plural'),
        'person': ('1', '1st (excl) Person')
    },
    
    # 1st (incl) Person, Dual
    {
        'alignment': ('A', 'A'),
        'gender': None,
        'number': ('du', 'Dual'),
        'person': ('12', '1st (incl) Person')
    },
    {
        'alignment': ('S', 'S'),
        'gender': None,
        'number': ('du', 'Dual'),
        'person': ('12', '1st (incl) Person')
    },
    {
        'alignment': ('O', 'O'),
        'gender': None,
        'number': ('du', 'Dual'),
        'person': ('12', '1st (incl) Person')
    },
    {
        'alignment': ('P', 'Possessive'),
        'gender': None,
        'number': ('du', 'Dual'),
        'person': ('12', '1st (incl) Person')
    },
    
    # 1st (incl) Person, Plural
    {
        'alignment': ('A', 'A'),
        'gender': None,
        'number': ('pl', 'Plural'),
        'person': ('12', '1st (incl) Person')
    },
    {
        'alignment': ('S', 'S'),
        'gender': None,
        'number': ('pl', 'Plural'),
        'person': ('12', '1st (incl) Person')
    },
    {
        'alignment': ('O', 'O'),
        'gender': None,
        'number': ('pl', 'Plural'),
        'person': ('12', '1st (incl) Person')
    },
    {
        'alignment': ('P', 'Possessive'),
        'gender': None,
        'number': ('pl', 'Plural'),
        'person': ('12', '1st (incl) Person')
    },
    
    # 2nd person Sg.
    {
        'alignment': ('A', 'A'),
        'gender': None,
        'number': ('sg', 'Singular'),
        'person': ('2', '2nd Person')
    },
    {
        'alignment': ('S', 'S'),
        'gender': None,
        'number': ('sg', 'Singular'),
        'person': ('2', '2nd Person')
    },
    {
        'alignment': ('O', 'O'),
        'gender': None,
        'number': ('sg', 'Singular'),
        'person': ('2', '2nd Person')
    },
    {
        'alignment': ('P', 'Possessive'),
        'gender': None,
        'number': ('sg', 'Singular'),
        'person': ('2', '2nd Person')
    },
    # 2nd Person Dual. 
    {
        'alignment': ('A', 'A'),
        'gender': None,
        'number': ('du', 'Dual'),
        'person': ('2', '2nd Person')
    },
    {
        'alignment': ('S', 'S'),
        'gender': None,
        'number': ('du', 'Dual'),
        'person': ('2', '2nd Person')
    },
    {
        'alignment': ('O', 'O'),
        'gender': None,
        'number': ('du', 'Dual'),
        'person': ('2', '2nd Person')
    },
    {
        'alignment': ('P', 'Possessive'),
        'gender': None,
        'number': ('du', 'Dual'),
        'person': ('2', '2nd Person')
    },
    # 2nd Person, Plural
    {
        'alignment': ('A', 'A'),
        'gender': None,
        'number': ('pl', 'Plural'),
        'person': ('2', '2nd Person')
    },
    {
        'alignment': ('S', 'S'),
        'gender': None,
        'number': ('pl', 'Plural'),
        'person': ('2', '2nd Person')
    },
    {
        'alignment': ('O', 'O'),
        'gender': None,
        'number': ('pl', 'Plural'),
        'person': ('2', '2nd Person')
    },
    {
        'alignment': ('P', 'Possessive'),
        'gender': None,
        'number': ('pl', 'Plural'),
        'person': ('2', '2nd Person')
    },
    # 3rd Person ----- INCLUDES GENDER
    {
        'alignment': ('A', 'A'),
        'gender': ('M', 'Masculine'),
        'number': ('sg', 'Singular'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('S', 'S'),
        'gender': ('M', 'Masculine'),
        'number': ('sg', 'Singular'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('O', 'O'),
        'gender': ('M', 'Masculine'),
        'number': ('sg', 'Singular'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('P', 'Possessive'),
        'gender': ('M', 'Masculine'),
        'number': ('sg', 'Singular'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('A', 'A'),
        'gender': ('F', 'Feminine'),
        'number': ('sg', 'Singular'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('S', 'S'),
        'gender': ('F', 'Feminine'),
        'number': ('sg', 'Singular'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('O', 'O'),
        'gender': ('F', 'Feminine'),
        'number': ('sg', 'Singular'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('P', 'Possessive'),
        'gender': ('F', 'Feminine'),
        'number': ('sg', 'Singular'),
        'person': ('3', '3rd Person')
    },
    {   
        'alignment': ('A', 'A'),
        'gender': ('N', 'Neuter'),
        'number': ('sg', 'Singular'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('S', 'S'),
        'gender': ('N', 'Neuter'),
        'number': ('sg', 'Singular'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('O', 'O'),
        'gender': ('N', 'Neuter'),
        'number': ('sg', 'Singular'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('P', 'Possessive'),
        'gender': ('N', 'Neuter'),
        'number': ('sg', 'Singular'),
        'person': ('3', '3rd Person')},
    {
        'alignment': ('A', 'A'),
        'gender': ('M', 'Masculine'),
        'number': ('du', 'Dual'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('S', 'S'),
        'gender': ('M', 'Masculine'),
        'number': ('du', 'Dual'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('O', 'O'),
        'gender': ('M', 'Masculine'),
        'number': ('du', 'Dual'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('P', 'Possessive'),
        'gender': ('M', 'Masculine'),
        'number': ('du', 'Dual'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('A', 'A'),
        'gender': ('F', 'Feminine'),
        'number': ('du', 'Dual'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('S', 'S'),
        'gender': ('F', 'Feminine'),
        'number': ('du', 'Dual'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('O', 'O'),
        'gender': ('F', 'Feminine'),
        'number': ('du', 'Dual'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('P', 'Possessive'),
        'gender': ('F', 'Feminine'),
        'number': ('du', 'Dual'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('A', 'A'),
        'gender': ('N', 'Neuter'),
        'number': ('du', 'Dual'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('S', 'S'),
        'gender': ('N', 'Neuter'),
        'number': ('du', 'Dual'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('O', 'O'),
        'gender': ('N', 'Neuter'),
        'number': ('du', 'Dual'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('P', 'Possessive'),
        'gender': ('N', 'Neuter'),
        'number': ('du', 'Dual'),
        'person': ('3', '3rd Person')},
    {
        'alignment': ('A', 'A'),
        'gender': ('M', 'Masculine'),
        'number': ('pl', 'Plural'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('S', 'S'),
        'gender': ('M', 'Masculine'),
        'number': ('pl', 'Plural'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('O', 'O'),
        'gender': ('M', 'Masculine'),
        'number': ('pl', 'Plural'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('P', 'Possessive'),
        'gender': ('M', 'Masculine'),
        'number': ('pl', 'Plural'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('A', 'A'),
        'gender': ('F', 'Feminine'),
        'number': ('pl', 'Plural'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('S', 'S'),
        'gender': ('F', 'Feminine'),
        'number': ('pl', 'Plural'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('O', 'O'),
        'gender': ('F', 'Feminine'),
        'number': ('pl', 'Plural'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('P', 'Possessive'),
        'gender': ('F', 'Feminine'),
        'number': ('pl', 'Plural'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('A', 'A'),
        'gender': ('N', 'Neuter'),
        'number': ('pl', 'Plural'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('S', 'S'),
        'gender': ('N', 'Neuter'),
        'number': ('pl', 'Plural'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('O', 'O'),
        'gender': ('N', 'Neuter'),
        'number': ('pl', 'Plural'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('P', 'Possessive'),
        'gender': ('N', 'Neuter'),
        'number': ('pl', 'Plural'),
        'person': ('3', '3rd Person')
    }
]


class Paradigm(TrackedModel):
    """Paradigm Details"""
    language = models.ForeignKey(Language)
    source = models.ForeignKey(Source)
    comment = models.TextField(blank=True, null=True,
        help_text="Comment on this paradigm")
    
    def __unicode__(self):
        return "Paradigm: %s" % self.language.slug
    
    def save(self, *args, **kwargs):
        if not self.pk:
            do_prefill = True
        else:
            do_prefill = False
        super(Paradigm, self).save(*args, **kwargs)
        
        if do_prefill:
            self._prefill_pronouns() # Prefill Pronouns
    
    def _prefill_pronouns(self):
        ed = User.objects.get(pk=1)
        existing_pronouns = self.pronoun_set.all()
        
        for comb in Pronoun._generate_all_combinations():
            NEEDED = True
            gender = None if comb['gender'] is None else comb['gender'][0]
            for e in existing_pronouns:
                old = (e.gender, e.number, e.person, e.alignment)
                new = (gender, comb['number'][0], comb['person'][0], comb['alignment'][0])
                if old == new:
                    NEEDED = False
                    break
            
            if NEEDED:
                obj = Pronoun.objects.create(
                    editor = ed,
                    paradigm = self,
                    person = comb['person'][0],
                    number = comb['number'][0],
                    alignment = comb['alignment'][0],
                    gender = gender
                )
                obj.save()
    
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
        ("N", "Neuter"),
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
    entries = models.ManyToManyField('lexicon.Lexicon', null=True, blank=True)
    
    def __unicode__(self):
        return '%s%s %s' % (self.person, self.number, self.alignment)
    
    @staticmethod
    def _generate_all_combinations():
        return PronounCombinations
        
    @staticmethod
    def _generate_all_rows():
        out, seen = [], []
        # Each combination of gender, number and person
        for p in Pronoun._generate_all_combinations():
            p2 = p.copy()
            del(p2['alignment'])
            if p2 not in seen:
                out.append(p2)
                seen.append(p2)
        return out

    
    @staticmethod
    def _get_row_size():
        return len(Pronoun.ALIGNMENT_CHOICES)
    
    class Meta:
        db_table = 'pronouns'
        

class PronounRelationshipManager(models.Manager):
    def get_relationships_for_pronoun(self, pronoun):
        return self.filter(models.Q(pronoun1=pronoun) | models.Q(pronoun2=pronoun))
    
    def has_relationship_between(self, pronoun1, pronoun2): 
        qset = self.filter(
            models.Q(pronoun1=pronoun1) & models.Q(pronoun2=pronoun2) | 
            models.Q(pronoun1=pronoun2) & models.Q(pronoun2=pronoun1)
        )
        if len(qset) == 0:
            return False
        else:
            return qset


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
    
    objects = PronounRelationshipManager()
    
    def __unicode__(self):
        return '<Relationship: %s-%s>' % (self.pronoun1, self.pronoun2)

    class Meta:
        db_table = 'pronoun_relationships'
        

class Rule(TrackedModel):
    """Pronoun Relationship Rules"""
    paradigm = models.ForeignKey('Paradigm')
    rule = models.CharField(max_length=64)
    relationships = models.ManyToManyField('Relationship', blank=True, null=True)
    
    def __unicode__(self):
        return '<Rule: %d-%s>' % (self.paradigm, self.rule)

    class Meta:
        db_table = 'pronoun_rules'

        