# -*- coding: utf-8 -*-
import os
import codecs
from django.db import transaction
from django.core.management.base import BaseCommand

from website.apps.core.models import Language
from website.apps.pronouns.models import Paradigm
from website.apps.pronouns.tools import copy_paradigm

class Command(BaseCommand):
    args = '<paradigm_id language_id>'
    help = 'Copies the paradigm `paradigm_id` to a new paradigm for `language_id'
    
    def handle(self, *args, **options):
        p = Paradigm.objects.get(pk=args[0])
        l = Language.objects.get(pk=args[1])
        copy_paradigm(p, l)
        