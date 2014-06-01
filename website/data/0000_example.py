#!/usr/bin/env python
#coding=utf-8
from django.contrib.auth.models import User

# import models
from website.apps.core.models import Source

# importer sets some variables
import os
print os.environ['IMPORTER_SITEROOT'] # the site root
print os.environ['IMPORTER_DATAROOT'] # the root of the data dir
print os.environ['IMPORTER_FILENAME'] # the filename currently being imported




# get editor
ed = User.objects.get(pk=1)

s = Source.objects.create(year=1111, author="Simon", slug="simon",
                          reference="simon 1111", bibtex="", comment="",
                          editor=ed)

# NOTE: if you get UnicodeDecodeErrors make sure you're using u"var" instead of "var"

# NOTES: you cannot use get_or_create because of - 
# django.db.transaction.TransactionManagementError: Your database backend
# doesn't behave properly when autocommit is off. Turn it on before using
# 'atomic'.

