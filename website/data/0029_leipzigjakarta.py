#!/usr/bin/env python
LEIPZIG_JAKARTA = """
fire
nose
to go
water
mouth
tongue
blood
bone
you
root
to come
breast
to rain
i
name
louse
wing
meat
arm-hand
fly-sp
night
ear
neck
far
to do-make
house
stone
bitter
to say 
tooth
hair
big
one
who
he-she
to hit
leg-foot
horn
this
fish
yesterday
to drink
black
navel
to stand
to bite
back
wind
smoke
what
child
egg
to give
new
to-burn
not
good
to know
knee
sand
to laugh 
to hear
earth
leaf
red 
liver
to hide
skin
to suck
to carry
ant
heavy
take
old
to eat
thigh
thick
long
to blow
stick
to run
to fall
eye
ashes
tail
dog
to cry
to tie
to see
sweet
rope
shadow
bird
salt
small
wide
star
in
hard
to crush
"""

from django.contrib.auth.models import User

# import models
from website.apps.lexicon.models import Word, WordSubset

# get editor
ed = User.objects.get(pk=1)

LPZJK = WordSubset.objects.create(
    subset="Leipzig-Jakarta List",
    slug="leipzig-jakarta",
    description="Tadmor et al. 2010",
    editor=ed
)

errors = 0
for slug in LEIPZIG_JAKARTA.split("\n"):
    slug = slug.strip()
    slug = slug.replace(" ", "-")
    if len(slug) == 0:
        continue
        
    try:
        w = Word.objects.get(slug=slug)
        print("{:10s}:{}".format(slug, w.slug))
    except Word.DoesNotExist:
        print("ERROR: Missing {}".format(slug))
        errors += 1
    
    LPZJK.words.add(w)
    
    
LPZJK.save()

if errors:
    raise ValueError("Too many errors: {}".format(errors))


s =  WordSubset.objects.get(slug="leipzig-jakarta").words.count()
print("{} words saved to Leipzig-Jakart list".format(s))