import csv
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import transaction
from reversion import revisions as reversion

from website.apps.core.models import Language


def read_glottolog(cldf_dir):
    """Returns ({glottocode: languages.csv row}, {glottocode: [ancestor glottocodes]})"""
    d = Path(cldf_dir)
    with open(d / 'languages.csv', newline='') as f:
        langs = {r['ID']: r for r in csv.DictReader(f)}
    with open(d / 'values.csv', newline='') as f:
        paths = {
            r['Language_ID']: [g for g in r['Value'].split('/') if g]
            for r in csv.DictReader(f) if r['Parameter_ID'] == 'classification'
        }
    return langs, paths


def classification(glottocode, langs, paths):
    """Family-level ancestor names (plus the node itself if it is a family, e.g. for
    proto-languages) joined by ', '; isolates get the language name"""
    lineage = paths.get(glottocode, []) + [glottocode]
    families = [langs[g]['Name'] for g in lineage if langs[g]['Level'] == 'family']
    if families:
        return ', '.join(families)
    row = langs[glottocode]
    if row['Level'] == 'dialect' and row['Language_ID']:
        row = langs[row['Language_ID']]
    return row['Name']


class Command(BaseCommand):
    help = 'Sets Language.classification from a glottolog-cldf checkout (dry run unless --apply)'

    def add_arguments(self, parser):
        parser.add_argument('cldf', help='glottolog-cldf "cldf" directory')
        parser.add_argument('--apply', action='store_true', help='save changes')

    def handle(self, *args, **options):
        langs, paths = read_glottolog(options['cldf'])
        changes, skipped = [], []
        for lang in Language.objects.order_by('slug'):
            if lang.glottocode not in langs:
                skipped.append(f'{lang.slug}\t{lang.glottocode or "(no glottocode)"}')
                continue
            new = classification(lang.glottocode, langs, paths)
            if new != (lang.classification or ''):
                changes.append((lang, new))

        for lang, new in changes:
            self.stdout.write(f'{lang.slug}\t{lang.glottocode}\n  - {lang.classification}\n  + {new}')
        self.stdout.write(f'\nSkipped ({len(skipped)}):\n' + '\n'.join(skipped))
        self.stdout.write(f'\n{len(changes)} changes' + ('' if options['apply'] else ' (dry run, use --apply)'))

        if options['apply']:
            with transaction.atomic(), reversion.create_revision():
                reversion.set_comment(f'sync_classification from {options["cldf"]}')
                for lang, new in changes:
                    lang.classification = new
                    lang.save()
