from django.utils import six
from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible

from reversion import revisions as reversion

from website.apps.core.models import TrackedModel, Language, Source

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
    ('M', 'Gender 1'),
    ('F', 'Feminine'),
    ('N', 'Gender 2'),
)

ANALECT_TYPES = (
    ('F', 'Free'),
    ('B', 'Bound'),
)


class ActivePronounTypeManager(models.Manager):
    """Hides inactive pronouns"""
    def get_queryset(self):
        return super(
            ActivePronounTypeManager, self
        ).get_queryset().filter(active=True)


@python_2_unicode_compatible
@reversion.register
class PronounType(TrackedModel):
    """Types of Pronouns"""
    alignment = models.CharField(max_length=1, choices=ALIGNMENT_CHOICES,
        help_text="Alignment")
    person = models.CharField(max_length=2, choices=PERSON_CHOICES,
        help_text="Person")
    number = models.CharField(max_length=2, choices=NUMBER_CHOICES,
        help_text="Number")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,
        blank=True, null=True,
        help_text="Gender")
    active = models.BooleanField(
        default=True, db_index=True,
        help_text="Show on website?"
    )
    sequence = models.PositiveSmallIntegerField(db_index=True, unique=True)
    word = models.ForeignKey('lexicon.Word')
    
    objects = ActivePronounTypeManager()
    
    def __str__(self):
        return six.text_type('%s%s %s' % (self.person, self.number, self.alignment))
    
    @staticmethod
    def _generate_all_combinations():
        qset = PronounType.objects.all()
        return qset.filter(active=True).order_by("sequence")
    
    @staticmethod
    def _get_row_size():
        return len(PronounType.ALIGNMENT_CHOICES)
    
    @staticmethod
    def _generate_all_rows():
        out, seen = [], []
        # Each combination of gender, number and person
        for ptype in PronounType._generate_all_combinations():
            p = {
                # no alignment
                'number': (ptype.number, ptype.get_number_display()),
                'person': (ptype.person, ptype.get_person_display()),
                'gender': None
            }
            if ptype.gender is not None:
                p['gender'] = (ptype.gender, ptype.get_gender_display())
            
            if p not in seen:
                out.append(p)
                seen.append(p)
        return out
    

@python_2_unicode_compatible
@reversion.register
class Paradigm(TrackedModel):
    """Paradigm Details"""
    language = models.ForeignKey(Language)
    source = models.ForeignKey(Source)
    comment = models.TextField(
        blank=True, null=True,
        help_text="Comment on this paradigm"
    )
    analect = models.CharField(
        max_length=1, choices=ANALECT_TYPES,
        blank=True, null=True,
        help_text="System Type"
    )
    label = models.CharField(
        max_length=32,
        blank=True, null=True,
        help_text="Short label"
    )
    
    def __str__(self):
        if self.label:
            return six.text_type("%s: %s" % (unicode(self.language), self.label))
        else:
            return six.text_type("%s" % unicode(self.language))
    
    def save(self, *args, **kwargs):
        if not self.pk:
            do_prefill = True
        else:
            do_prefill = False
        super(Paradigm, self).save(*args, **kwargs)
        
        if do_prefill:
            self._prefill_pronouns()
    
    def _prefill_pronouns(self):
        editor = User.objects.all().order_by('id')[0]
        # figure out the pronouns we already have
        existing_pronouns = []
        for e in self.pronoun_set.select_related().all():
            token = (e.pronountype.gender, e.pronountype.number,
                     e.pronountype.person, e.pronountype.alignment)
            existing_pronouns.append(token)
        
        for p in PronounType._generate_all_combinations():
            token = (p.gender, p.number, p.person, p.alignment)
            if token not in existing_pronouns:
                obj = Pronoun.objects.create(
                    editor=editor,
                    paradigm=self,
                    pronountype=p,
                )
                obj.save()
    
    @models.permalink
    def get_absolute_url(self):
        return ('pronouns:detail', [self.id])
    
    class Meta:
        db_table = 'paradigms'
        


@python_2_unicode_compatible
@reversion.register
class Pronoun(TrackedModel):
    """Pronoun Data"""
    paradigm = models.ForeignKey('Paradigm')
    pronountype = models.ForeignKey('PronounType')
    comment = models.TextField(blank=True, null=True,
        help_text="Comment on this paradigm")
    entries = models.ManyToManyField('lexicon.Lexicon', blank=True)
    
    def __str__(self):
        return six.text_type('%s' % self.pronountype)
    
    @staticmethod
    def _generate_all_rows():
        out, seen = [], []
        # Each combination of gender, number and person
        for p in PronounType._generate_all_combinations():
            p2 = p.copy()
            del(p2['alignment'])
            if p2 not in seen:
                out.append(p2)
                seen.append(p2)
        return out
    
    class Meta:
        db_table = 'pronouns'
        

class PronounRelationshipManager(models.Manager):
    
    def _get_pk(self, thing):
        if hasattr(thing, 'pk'):
            return thing.pk
        elif type(thing) == int:
            return thing
        else:
            raise ValueError("Unable to identify the PK of %r" % thing)
    
    def get_relationships_for_pronoun(self, pronoun):
        return self.filter(
            models.Q(pronoun1_id=self._get_pk(pronoun)) |
            models.Q(pronoun2_id=self._get_pk(pronoun))
        )
    
    def has_relationship_between(self, pronoun1, pronoun2):
        ppk1, ppk2 = self._get_pk(pronoun1), self._get_pk(pronoun2)
        qset = self.filter(
            models.Q(pronoun1_id=ppk1) & models.Q(pronoun2_id=ppk2) |
            models.Q(pronoun1_id=ppk2) & models.Q(pronoun2_id=ppk1)
        )
        if len(qset) > 0:
            return True
        else:
            return False


@python_2_unicode_compatible
@reversion.register
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
        help_text="Comment on this relationship")
    
    objects = PronounRelationshipManager()
    
    def __str__(self):
        return six.text_type('%s-%s' % (self.pronoun1, self.pronoun2))
        
    class Meta:
        db_table = 'pronoun_relationships'
        

@python_2_unicode_compatible
@reversion.register
class Rule(TrackedModel):
    """Pronoun Relationship Rules"""
    paradigm = models.ForeignKey('Paradigm')
    rule = models.CharField(max_length=64)
    relationships = models.ManyToManyField('Relationship', blank=True)
    
    def __str__(self):
        return six.text_type('%d-%s' % (self.paradigm.id, self.rule))
        
    class Meta:
        db_table = 'pronoun_rules'

        
