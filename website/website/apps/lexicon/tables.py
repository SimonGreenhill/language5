from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.utils.html import escape

import django_tables2 as tables
from django_tables2.utils import A  # alias for Accessor

from website.apps.core.tables import DataTable

from website.apps.lexicon.models import Word, WordSubset, Cognate


class WordIndexTable(DataTable):
    """Word Listing"""
    id = tables.LinkColumn('word-detail', args=[A('slug')])
    word = tables.LinkColumn('word-detail', args=[A('slug')])
    
    class Meta(DataTable.Meta):
        model = Word
        order_by_field = 'word' # default sorting
        sequence = ('id', 'word')
        exclude = ('editor', 'added', 'slug', 'full')

