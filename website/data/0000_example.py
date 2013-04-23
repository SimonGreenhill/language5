#!/usr/bin/env python
from django.contrib.auth.models import User

# import models
from website.apps.core.models import Source

# get editor
ed = User.objects.get(pk=1)

s = Source.objects.create(year=1111, author="Simon", slug="simon",
                          reference="simon 1111", bibtex="", comment="",
                          editor=ed)

# NOTE: if you get UnicodeDecodeErrors make sure you're using u"var" instead of "var"
