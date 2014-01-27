from django.db.models import Count
from django.http import Http404
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from django.shortcuts import get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from website.apps.lexicon.models import Word, WordSubset, Lexicon, Cognate

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
        context['lexicon'] = WordLexiconTable(kwargs['object'].lexicon_set.select_related().all())
        try:
            context['lexicon'].paginate(page=self.request.GET.get('page', 1), per_page=50)
        except EmptyPage: # 404 on a empty page
            raise Http404
        except PageNotAnInteger: # 404 on invalid page number
            raise Http404
        return context


class LexiconDetail(DetailView):
    """Lexicon Detail"""
    model = Lexicon
    template_name = 'lexicon/lexicon_detail.html'

#@reversion.create_revision()

class LexiconEdit(UpdateView):
    """Lexicon Editor"""
    model = Lexicon
    #fields = ['name'] ? necc?
    template_name_suffix = '_edit'
    
    def form_valid(self, form):
        # TODO: set editor and timestamp and reversion
        return super(LexiconEdit, self).form_valid(form)
            
    # have to be logged in!
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LexiconEdit, self).dispatch(*args, **kwargs)
