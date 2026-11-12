from collections import Counter

from django.contrib.auth.models import User
from django.contrib.redirects.models import Redirect
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.urls import reverse
from django.utils.text import slugify
from reversion import revisions as reversion

from website.apps.core.management.commands.sync_classification import read_glottolog
from website.apps.core.models import Family, Language


def family_url(slug):
    return reverse('family-detail', kwargs={'slug': slug})


class Command(BaseCommand):
    help = ('Sets Language.family to the top-level Glottolog family (isolates get their own) '
            'from a glottolog-cldf checkout (dry run unless --apply)')

    def add_arguments(self, parser):
        parser.add_argument('cldf', help='glottolog-cldf "cldf" directory')
        parser.add_argument('--apply', action='store_true', help='save changes')
        parser.add_argument('--drop', nargs='+', default=[], metavar='SLUG',
                            help='families to delete without a redirect (their URLs 404)')

    def handle(self, *args, **options):
        langs, paths = self.glottolog = read_glottolog(options["cldf"])
        name = lambda gc: langs[gc]['Name']
        slug = lambda gc: slugify(name(gc))[:64]

        languages = list(Language.objects.prefetch_related('family').order_by('slug'))
        target = {
            lang.pk: (paths.get(lang.glottocode, []) + [lang.glottocode])[0]
            for lang in languages if lang.glottocode in langs
        }
        families = {f.pk: f for f in Family.objects.all()}

        # existing family row for each target: same glottocode, else the old family
        # sharing the most languages with it (renamed in place)
        claimed = {f.glottocode: f for f in families.values() if f.glottocode in target.values()}
        overlap = Counter(
            (f.pk, target[lang.pk]) for lang in languages if lang.pk in target for f in lang.family.all()
        )
        successors = {pk: [gc for (p, gc), _ in overlap.most_common() if p == pk] for pk in families}
        dropped = {f.pk for f in families.values() if f.slug in options['drop']}
        for (pk, gc), _ in overlap.most_common():
            if gc not in claimed and pk not in dropped and families[pk] not in claimed.values():
                claimed[gc] = families[pk]

        renames = [(f, gc) for gc, f in claimed.items()
                   if (f.slug, f.family, f.glottocode) != (slug(gc), name(gc), gc)]
        creates = sorted(set(target.values()) - set(claimed), key=name)
        deletes = []
        for f in families.values():
            if f in claimed.values():
                continue
            if f.pk in dropped:
                deletes.append((f, None))
            elif successors[f.pk]:
                deletes.append((f, family_url(slug(successors[f.pk][0]))))
            else:
                deletes.append((f, reverse('family-index')))
        moves = [
            (lang, target.get(lang.pk))
            for lang in languages
            if {f.pk for f in lang.family.all()} != (
                {claimed[target[lang.pk]].pk} if lang.pk in target and target[lang.pk] in claimed else set())
        ]

        for f, gc in renames:
            self.stdout.write(f'rename\t{f.slug} -> {slug(gc)}\t{name(gc)} ({gc})')
        for gc in creates:
            self.stdout.write(f'create\t{slug(gc)}\t{name(gc)} ({gc})')
        for f, url in deletes:
            self.stdout.write(f'delete\t{f.slug}\t' + (f'redirect -> {url}' if url else '404'))
        for lang, gc in moves:
            if gc is None:
                self.stdout.write(f'no family\t{lang.slug}\t{lang.glottocode or "(no glottocode)"}')
        self.stdout.write(
            f'\n{len(renames)} renamed, {len(creates)} created, {len(deletes)} deleted, '
            f'{len(moves)} languages changed' + ('' if options['apply'] else ' (dry run, use --apply)'))

        if options['apply']:
            with transaction.atomic(), reversion.create_revision():
                reversion.set_comment(f'sync_families from {options["cldf"]}')
                self.apply(renames, creates, deletes, claimed, target, languages, name, slug)

    def apply(self, renames, creates, deletes, claimed, target, languages, name, slug):
        site = Site.objects.get_current()
        for f, url in deletes:
            old = f.get_absolute_url()
            if url:
                Redirect.objects.filter(new_path=old).update(new_path=url)
                Redirect.objects.update_or_create(site=site, old_path=old, defaults={'new_path': url})
            else:
                Redirect.objects.filter(new_path=old).delete()
            f.delete()

        # rename in place (pre_save creates the redirect); defer rows whose new
        # slug/name is still held by another family that has yet to be renamed
        pending = list(renames)
        while pending:
            waiting = []
            for f, gc in pending:
                taken = Family.objects.exclude(pk=f.pk).filter(slug=slug(gc)).exists() or \
                    Family.objects.exclude(pk=f.pk).filter(family=name(gc)).exists()
                if taken:
                    waiting.append((f, gc))
                    continue
                f.slug, f.family, f.glottocode = slug(gc), name(gc), gc
                f.save()
            if len(waiting) == len(pending):
                raise CommandError(f'Cannot rename, names in use: {[gc for _, gc in waiting]}')
            pending = waiting

        editor = User.objects.filter(is_superuser=True).order_by('pk').first()
        if creates and editor is None:
            raise CommandError('Need a superuser as editor for new families')
        for gc in creates:
            claimed[gc] = Family.objects.create(family=name(gc), slug=slug(gc), glottocode=gc, editor=editor)

        for lang in languages:
            lang.family.set([claimed[target[lang.pk]]] if lang.pk in target else [])

        # each family's Glottolog subtree, for the coverage tree on family pages;
        # update() skips reversion and the redirect signal
        langs, paths = self.glottolog
        trees = {gc: {} for gc in claimed}
        for gc, row in langs.items():
            lineage = paths.get(gc, [])
            root = lineage[0] if lineage else gc
            if root in trees:
                trees[root][gc] = [row['Name'], row['Level'], lineage[-1] if lineage else None]
        for gc, f in claimed.items():
            Family.objects.filter(pk=f.pk).update(glottolog_tree=trees[gc])
