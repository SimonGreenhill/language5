from django.db.models import Count

from website.apps.lexicon.models import Word, WordSubset, Cognate

from django_tables2 import SingleTableView
from website.apps.lexicon.tables import WordIndexTable


class WordIndex(SingleTableView):
    """Word Index"""
    model = Word
    template_name = 'lexicon/word_index.html'
    table_class = WordIndexTable
    table_pagination = {"per_page": 50}
