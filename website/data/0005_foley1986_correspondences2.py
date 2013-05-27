# -*- coding: utf-8 -*-
from django.contrib.auth.models import User

# import models
from website.apps.core.models import Source, Language, AlternateName, Family
from website.apps.lexicon.models import Correspondence, CorrespondenceSet

ED = User.objects.get(pk=1)
SOURCE = Source.objects.get(slug="foley1986")

# P Y K A C M
LANGUAGES = [
    Language.objects.get(slug="proto-lower-sepik"),
    Language.objects.get(slug="yimas"),
    Language.objects.get(slug="tabriak"),
    Language.objects.get(slug="angoram"),
    Language.objects.get(slug="chambri"),
    Language.objects.get(slug="murik"),
]


corr = u"""*mp mb mb mb mp b
*ŋk ŋg ŋg ŋg ŋk (ŋ)g
*ŋg ŋg ŋg 0 ŋg k
*ng nd nd nd nd d/nd"""

total_counter = 0
total_corrs = len(corr.split("\n"))


for line in corr.split("\n"):
    line = line.strip().split(" ")
    assert len(line) == len(LANGUAGES)
    print line
    corrset = CorrespondenceSet.objects.create(source=SOURCE, editor=ED,
                                               comment="Proto-Lower-Sepik %s" % line[0])
    corrset.save()
    counter = 0
    for i, c in enumerate(line):
        if c != 0:
            print i, c
            lang = LANGUAGES[i]
            o = Correspondence.objects.create(language=lang, rule=c, editor=ED, corrset=corrset)
            o.save()
            counter += 1
        assert len(corrset.correspondence_set.all()) == counter
    total_counter += counter
    
