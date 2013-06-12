from django.db.models import Count
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404

from website.apps.lexicon.models import Word, WordSubset, Cognate

from django_tables2 import SingleTableView
from website.apps.lexicon.tables import WordIndexTable, WordLexiconTable


class WordIndex(SingleTableView):
    """Word Index"""
    model = Word
    template_name = 'lexicon/word_index.html'
    table_class = WordIndexTable
    table_pagination = {"per_page": 50}
    
    def get_queryset(self):
        if 'subset' in self.request.GET:
            self.subset = get_object_or_404(WordSubset, slug=self.request.GET['subset'])
            return self.subset.words.all().annotate(count=Count("lexicon"))
        else:
            self.subset = None
            return Word.objects.annotate(count=Count('lexicon'))
    
    def get_context_data(self, **kwargs):
        context = super(WordIndex, self).get_context_data(**kwargs)
        context['subset'] = self.subset
        context['subsets'] = WordSubset.objects.all()
        return context
    

class WordDetail(DetailView):
    """Word Detail"""
    model = Word
    template_name = 'lexicon/word_detail.html'
    table_class = WordLexiconTable
    table_pagination = {"per_page": 50}
    
    def get_context_data(self, **kwargs):
        context = super(WordDetail, self).get_context_data(**kwargs)
        table = WordLexiconTable(kwargs['object'].lexicon_set.select_related().all())
        table.paginate(page=self.request.GET.get('page', 1), per_page=50)
        context['lexicon'] = table
        return context
