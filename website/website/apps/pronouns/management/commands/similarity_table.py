# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from website.apps.pronouns.models import Paradigm, Pronoun
from website.apps.pronouns.tools import short_repr_row, PronounFinder

class Command(BaseCommand):
    args = '<paradigm_id>'
    help = 'Displays a pronoun table'
    
    def handle(self, *args, **options):
        pdm = Paradigm.objects.get(pk=args[0])
        pf = PronounFinder()
        labels = [short_repr_row(p) for p in Pronoun._generate_all_combinations()]
        data = {}
        for p1 in pdm.pronoun_set.all():
            p1_id = short_repr_row(p1)
            for p2 in pdm.pronoun_set.all():
                p2_id = short_repr_row(p2)
                if len(p1.form) == 0 or len(p2.form) == 0:
                    continue
                part1 = u"%s (%s)" % (p1_id, p1.form)
                part2 = u"%s (%s)" % (p2_id, p2.form)
                print part1.ljust(20), '::', part2.ljust(20), "%0.2f" % pf.compare(p1.form, p2.form)
