"""Family page tree: the family's Glottolog subtree with each TNG language placed
under its Glottolog language, and TNG coverage rolled up per subgroup"""
from collections import defaultdict

from django.utils.html import format_html, format_html_join
from django.utils.safestring import mark_safe

GLOTTOLOG = 'https://glottolog.org/resource/languoid/id/'
BINS = [(0, 'b0', '0'), (100, 'b1', '1–100'), (200, 'b2', '101–200'), (500, 'b3', '201–500'), (None, 'b4', '500+')]


def items_bin(n):
    return next(c for limit, c, _ in BINS if limit is None or n <= limit)


class Tree:
    def __init__(self, nodes, languages):
        """nodes: Family.glottolog_tree; languages: TNG languages annotated with `count`"""
        self.nodes = nodes
        self.kids = defaultdict(list)
        for gc, (name, level, parent) in nodes.items():
            if parent and level != 'dialect':
                self.kids[parent].append(gc)
        self.root = next((gc for gc, (_, _, parent) in nodes.items() if parent is None), None)
        self.tng, self.unplaced = defaultdict(list), []
        for lang in languages:
            gc = self.place(lang.glottocode)
            (self.tng[gc] if gc else self.unplaced).append(lang)
        self.stats = {}
        if self.root:
            self.roll(self.root)

    def place(self, gc):
        """Tree node for a TNG glottocode: dialects go to their language"""
        while gc in self.nodes and self.nodes[gc][1] == 'dialect':
            gc = self.nodes[gc][2]
        return gc if gc in self.nodes else None

    def roll(self, gc):
        """(covered languages, total languages, items)"""
        is_lang = self.nodes[gc][1] == 'language'
        cov, tot = (int(gc in self.tng), 1) if is_lang else (0, 0)
        items = sum(lang.count for lang in self.tng.get(gc, []))
        for k in self.kids[gc]:
            c, t, i = self.roll(k)
            cov, tot, items = cov + c, tot + t, items + i
        self.stats[gc] = (cov, tot, items)
        return self.stats[gc]

    def html(self):
        return mark_safe(self.render(self.root, 0)) if self.root else ''

    # rendering
    def row(self, label, depth, cls, cov=None, tot=None, items=None, pill=False):
        coverage = format_html('{} / {}<span class="cov-bar"><i style="width:{}%"></i></span>',
                               cov, f'{tot:,}', round(100 * cov / tot)) if tot else ''
        count = '' if items is None else (
            format_html('<span class="pill {}">{}</span>', items_bin(items), f'{items:,}') if pill else f'{items:,}')
        return format_html('<div class="cov-row {}" style="--d:{}"><span class="cov-name">{}</span>'
                           '<span class="cov-num">{}</span><span class="cov-num">{}</span></div>',
                           cls, depth, label, coverage, count)

    def glottolog(self, gc):
        return format_html(' <a class="cov-code" href="{}{}">{}</a>', GLOTTOLOG, gc, gc)

    def tng_row(self, lang, depth, extra=''):
        label = format_html('<a href="{}">{}</a>{}', lang.get_absolute_url(), str(lang), extra)
        return self.row(label, depth, 'cov-lang' + ('' if lang.count else ' cov-empty'), items=lang.count, pill=True)

    def render(self, gc, depth):
        name, level, _ = self.nodes[gc]
        cov, tot, items = self.stats[gc]
        if level == 'language':
            langs = self.tng.get(gc, [])
            if not langs:
                return self.row(format_html('<a href="{}{}">{}</a>', GLOTTOLOG, gc, name), depth, 'cov-lang cov-missing')
            if len(langs) == 1 and not self.kids[gc]:
                return self.tng_row(langs[0], depth, self.glottolog(gc))
            children = ''.join(self.tng_row(lang, depth + 1) for lang in langs)
            cls = 'cov-clade cov-glang'
        else:
            children = ''.join(self.tng_row(lang, depth + 1, mark_safe(' <span class="cov-tag">proto</span>'))
                               for lang in self.tng.get(gc, []))
            order = sorted(self.kids[gc], key=lambda k: (not self.stats[k][0], -self.stats[k][2], self.nodes[k][0]))
            children += ''.join(self.render(k, depth + 1) for k in order)
            cls = 'cov-clade' + ('' if cov else ' cov-missing')
        summary = self.row(format_html('{}{}', name, self.glottolog(gc)), depth, cls, cov, tot, items if cov else None)
        # branches with data start open; empty (grey) ones collapsed
        return f'<details{" open" if cov else ""}><summary>{summary}</summary>{children}</details>'

    def legend(self):
        return format_html_join(' ', '<span class="pill {}">{}</span>', ((c, t) for _, c, t in BINS))
