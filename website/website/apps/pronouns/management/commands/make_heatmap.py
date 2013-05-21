# -*- coding: utf-8 -*-
import os
from django.core.management.base import BaseCommand
from website.apps.pronouns.models import Paradigm, Pronoun, Distance
from website.apps.pronouns.tools import short_repr_row, PronounFinder


import matplotlib.pyplot as plt
import numpy as np
from prettytable import PrettyTable


class Command(BaseCommand):
    args = '<paradigm_id>'
    help = 'Creates a heatmap'
    
    def handle(self, *args, **options):
        pdm = Paradigm.objects.get(pk=args[0])
        pf = PronounFinder()
        labels = [short_repr_row(p) for p in Pronoun._generate_all_combinations()]
        data = {}
        for p1 in pdm.pronoun_set.all():
            p1_id = short_repr_row(p1)
            for p2 in pdm.pronoun_set.all():
                p2_id = short_repr_row(p2)
                data[(p1_id, p2_id)] = pf.compare(p1.form, p2.form)
        
        rows = []
        for p1 in labels:
            row = []
            for p2 in labels:
                row.append(data.get((p1,p2), 0.0))
            rows.append(row)
        
        data = np.array(rows)
        
        # start plotting
        fig, axes = plt.subplots()
        heatmap = axes.pcolor(data, cmap=plt.cm.Blues)
        
        # put the major ticks at the middle of each cell
        axes.set_xticks(np.arange(data.shape[0])+0.5, minor=False)
        axes.set_yticks(np.arange(data.shape[1])+0.5, minor=False)
        
        # want a more natural, table-like display
        axes.invert_yaxis()
        
        # set labels
        axes.set_xticklabels(labels, minor=False, rotation=90, fontsize=5)
        axes.set_yticklabels(labels, minor=False, fontsize=5)
        
        plt.tick_params(direction="out")
        plt.tick_params(right="off")
        plt.tick_params(top="off")
        
        plt.suptitle(pdm.language)
        
        plt.savefig("%s-%d.png" % (pdm.language.slug, pdm.id))
        print("Written to %s-%d.png" % (pdm.language.slug, pdm.id))
        
        
        cols = ['-']
        cols.extend(labels)
        x = PrettyTable(cols)
        for i, row in enumerate(data):
            row = row.round(3)
            newrow = [labels[i]]
            for r in row:
                newrow.append(round(r, 3))
            x.add_row(newrow)
        
        with open("%s-%d.txt" % (pdm.language.slug, pdm.id), 'w+') as handle:
            handle.write(x.get_string())
        print("Written to %s-%d.txt" % (pdm.language.slug, pdm.id))
        
