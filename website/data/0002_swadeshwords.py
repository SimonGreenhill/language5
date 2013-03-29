#!/usr/bin/env python
import os
import sys
from datetime import datetime

from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from website.apps.lexicon.models import Word, WordSubset

me = User.objects.get(pk=1)

SWADESH100 = """
all | (of a number)
ashes
bark | (of tree)
belly
big
bird
black
blood
bone
breast
claw
cloud
cold | (of weather)
dog
dry | (substance)
ear
earth | (soil)
egg
eye
fat | (organic substance)
feather | (larger feathers rather than down)
fire
fish
foot
full
good
green
hair
hand
head
heart
horn
I
knee
leaf
liver
long
louse
man | (male human)
many
meat | (flesh)
moon
mountain
mouth
name
neck
new
night
nose
not
one
person
red
road | (or trail)
root
round
sand
seed
skin | (person's)
small
smoke | (of fire)
star
stone
sun
tail
that
this
thou
to bite
to burn | (intrans,).
to come
to die
to drink
to eat
to fly
to give
to hear
to kill
to know | (facts)
to lie | (on side)
to rain
to say
to see
to sit
to sleep
to stand
to swim
to walk
tongue
tooth | (front rather than molar)
tree
two
warm | (of weather)
water
we
what?
white
who?
woman
yellow
"""

SWADESH200 = """
and
animal
ashes
at
back | (person's)
bad | (deleterious or unsuitable)
bark | (of tree)
because
belly
berry | (or fruit)
big
bird
to bite
black
blood
to blow | (of wind)
bone
breathe
to burn | (intrans,).
child | (young person rather than as relationship term)
cloud
cold | (of weather)
to come
to count
to cut
day | (opposite of night rather than time measure)
to die
to dig
dirty
dog
to drink
dry | (substance)
dull | (knife)
dust
ear
earth | (soil)
to eat
egg
eye
to fall | (drop rather than topple)
far
fat | (organic substance)
father
to fear
feather | (larger feathers rather than down)
few
to fight
fire
fish
five
to float
to flow
flower
to fly
fog
foot
four
to freeze
to give
good
grass
green
guts
hair
hand
he
head
to hear
heart
heavy
here
to hit
to hold | (in hand)
how
to hunt | (game)
husband
I
ice
if
in
to kill
to know | (facts)
lake
to laugh
leaf
left (hand)
leg
to lie | (on side)
to live
liver
long
louse
man | (male human)
many
meat | (flesh)
mother
mountain
mouth
name
narrow
near
neck
new
night
nose
not
old
one
other
person
to play
to pull
to push
to rain
red
right (correct)
right (hand)
river
road | (or trail)
root
rope
rotten | (especially log)
to rub
salt
sand
to say
to scratch | (as with fingernails to relieve itch)
sea | (ocean)
to see
seed
to sew
sharp | (as knife)
short
to sing
to sit
skin | (person's)
sky
to sleep
small
to smell | (perceive odor)
smoke | (of fire)
smooth
snake
snow
some
to spit
to split
to squeeze
to stab | (or stick)
to stand
star
stick | (of wood)
stone
straight
to suck
sun
to swell
to swim
tail
that
there
they
thick
thin
to think
this
thou
three
to throw
to tie
tongue
tooth | (front rather than molar)
tree
to turn | (change one's direction)
two
to vomit
to walk
warm | (of weather)
to wash
water
we
wet
what?
when?
where?
white
who?
wide
wife
wind
wing
to wipe
with | (accompanying)
woman
woods
worm
ye
year
yellow
"""

    
# add all wordlist to WordSubset
sw100 = WordSubset.objects.create(
    subset="Swadesh 100",
    slug="swadesh-100",
    description="Swadesh 100-item Basic Vocabulary list",
    editor=me,
    added=datetime.now()
)
sw200 = WordSubset.objects.create(
    subset="Swadesh 200",
    slug="swadesh-200",
    description="Swadesh 200-item Basic Vocabulary list",
    editor=me,
    added=datetime.now()
)



wordlist100 = {}
for s in SWADESH100.split("\n"):
    s = s.strip()
    if len(s) > 0:
        if '|' in s:
            s, full_s = [_.strip() for _ in s.split("|")]
        else:
            full_s = ""
            
        print 'S100', s.ljust(20), full_s.ljust(20), slugify(s)
        
        w = Word.objects.create(
            word = s,
            slug = slugify(s),
            full = full_s,
            editor = me,
            added = datetime.now()
        )
        wordlist100[s] = w
        sw100.words.add(w)
        sw200.words.add(w)

for s in SWADESH200.split("\n"):
    s = s.strip()
    if len(s) > 0:
        if '|' in s:
            s, full_s = [_.strip() for _ in s.split("|")]
        else:
            full_s = ""
        
        if s not in wordlist100:
            print 'S200', s.ljust(20), full_s.ljust(20), slugify(s)
            w = Word.objects.create(
                word = s,
                slug = slugify(s),
                full = full_s,
                editor = me,
                added = datetime.now()
            )
            sw200.words.add(w)
        