from types import SimpleNamespace

from django.test import SimpleTestCase

from website.apps.core.coverage import Tree, items_bin

NODES = {
    'fama1234': ['Family A', 'family', None],
    'suba1234': ['Sub A', 'family', 'fama1234'],
    'lana1234': ['Lang A', 'language', 'suba1234'],
    'diaa1234': ['Dialect A', 'dialect', 'lana1234'],
    'lanb1234': ['Lang B', 'language', 'suba1234'],
    'subb1234': ['Sub B', 'family', 'fama1234'],
    'lanc1234': ['Lang C', 'language', 'subb1234'],
}


def lang(name, gc, count):
    return SimpleNamespace(language=name, glottocode=gc, count=count, __str__=None,
                           get_absolute_url=lambda: f'/language/{name}')


class TestTree(SimpleTestCase):
    def setUp(self):
        self.langs = [lang('a', 'lana1234', 50), lang('a-dial', 'diaa1234', 300),
                      lang('proto-a', 'suba1234', 10), lang('lost', None, 5), lang('wrong', 'xxxx1234', 1)]
        self.tree = Tree(NODES, self.langs)

    def test_placement(self):
        self.assertEqual(self.tree.root, 'fama1234')
        self.assertEqual([l.language for l in self.tree.tng['lana1234']], ['a', 'a-dial'])  # dialect -> language
        self.assertEqual([l.language for l in self.tree.tng['suba1234']], ['proto-a'])
        self.assertEqual([l.language for l in self.tree.unplaced], ['lost', 'wrong'])

    def test_rollup(self):
        self.assertEqual(self.tree.stats['fama1234'], (1, 3, 360))
        self.assertEqual(self.tree.stats['suba1234'], (1, 2, 360))
        self.assertEqual(self.tree.stats['subb1234'], (0, 1, 0))

    def test_html(self):
        html = self.tree.html()
        self.assertIn('1 / 3', html)
        self.assertIn('href="/language/a"', html)
        self.assertIn('https://glottolog.org/resource/languoid/id/lanc1234', html)  # uncovered: Glottolog link
        self.assertIn('cov-missing', html)
        self.assertNotIn('Dialect A', html)
        # covered subgroup listed before the uncovered one
        self.assertLess(html.index('Sub A'), html.index('Sub B'))

    def test_covered_branches_open(self):
        html = self.tree.html()
        self.assertEqual(html.count('<details open>'), 3)  # Family A, Sub A, Lang A
        self.assertEqual(html.count('<details>'), 1)  # Sub B has no data

    def test_empty_tree(self):
        tree = Tree({}, self.langs)
        self.assertIsNone(tree.root)
        self.assertEqual(tree.html(), '')

    def test_bins(self):
        self.assertEqual([items_bin(n) for n in (0, 100, 101, 500, 501)], ['b0', 'b1', 'b2', 'b3', 'b4'])
