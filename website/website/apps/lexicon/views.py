from string import ascii_uppercase

from django.core.paginator import EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import Http404
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.decorators import method_decorator
from django.utils import timezone

from website.apps.lexicon.models import Word, WordSubset, Lexicon
from website.apps.lexicon.forms import LexiconForm

from django_tables2 import SingleTableView, RequestConfig
from website.apps.core.crawler_trap import (
    CrawlerTrapMixin, canonical_sort_redirect, guard_page, list_seo_context
)
from website.apps.lexicon.tables import WordIndexTable, WordLexiconTable
from website.apps.lexicon.tables import WordLexiconEditTable

# for WordEdit
from django.forms.models import modelformset_factory
from website.apps.lexicon.forms import WordForm


class WordIndex(CrawlerTrapMixin, SingleTableView):
    """Word Index"""
    model = Word
    template_name = 'lexicon/word_index.html'
    table_class = WordIndexTable
    table_pagination = {"per_page": 50}
    
    def valid_subset(self, value):
        return super().valid_subset(value) or WordSubset.objects.filter(slug=value).exists()

    def get_queryset(self):
        # filter on subset if necessary
        self.subset = self.request.GET.get('subset', None)
        if self.subset:
            try:
                qset = WordSubset.objects.get(slug=self.subset).words.all()
            except WordSubset.DoesNotExist:
                qset = Word.objects.all().filter(word__istartswith=self.subset)
        else:
            qset = Word.objects.all()
        
        return qset.annotate(count=Count("lexicon")).order_by("word")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subset'] = self.subset
        context['subsets'] = WordSubset.objects.all()
        context['letters'] = [*ascii_uppercase]
        
        RequestConfig(self.request).configure(context['table'])
        
        try:
            context['table'].paginate(
                page=self.request.GET.get('page', 1), per_page=50
            )
        except EmptyPage:  # 404 on a empty page
            raise Http404
        except PageNotAnInteger:  # 404 on invalid page number
            raise Http404
        
        return context
    

class WordDetail(DetailView):
    """Word Detail"""
    model = Word
    template_name = 'lexicon/word_detail.html'
    table_class = WordLexiconTable
    table_pagination = {"per_page": 50}

    def get(self, request, *args, **kwargs):
        guard_page(request)
        if not request.user.is_authenticated:
            redirect = canonical_sort_redirect(request, WordLexiconTable)
            if redirect is not None:
                return redirect
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(list_seo_context(self.request))

        qset = kwargs['object'].lexicon_set.select_related().all()
        if self.request.user.is_authenticated:
            context['lexicon'] = WordLexiconEditTable(qset)
        else:
            context['lexicon'] = WordLexiconTable(qset)
        RequestConfig(self.request).configure(context['lexicon'])
            
        try:
            context['lexicon'].paginate(
                page=self.request.GET.get('page', 1), per_page=50
            )
        except EmptyPage:  # 404 on a empty page
            raise Http404
        except PageNotAnInteger:  # 404 on invalid page number
            raise Http404
        return context


class LexiconDetail(DetailView):
    """Lexicon Detail"""
    model = Lexicon
    template_name = 'lexicon/lexicon_detail.html'
        

class LexiconEdit(UpdateView):
    """Lexicon Editor"""
    model = Lexicon
    form_class = LexiconForm
    template_name_suffix = '_edit'
    
    def form_valid(self, form):
        from django.utils import timezone
        from reversion import revisions as reversion
        form.instance.editor = self.request.user
        form.instance.added = timezone.now()
        with reversion.create_revision():
            form.save()
        return super().form_valid(form)
    
    @method_decorator(login_required)  # ensure logged in
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)




@login_required()
def word_edit(request, slug):
    w = get_object_or_404(Word, slug=slug)
    GenericFormSet = modelformset_factory(Lexicon, form=WordForm, extra=0)
    formset = GenericFormSet(
        request.POST or None, queryset=w.lexicon_set.all()
    )
    # build each choice list once and share it, instead of one query per row
    choices = {}
    for form in formset:
        for name in ('language', 'source', 'word'):
            if name not in choices:
                choices[name] = list(form.fields[name].choices)
            form.fields[name].choices = choices[name]

    if request.POST and formset.is_valid():
        from reversion import revisions as reversion
        for form in formset:
            if form.is_valid() and len(form.changed_data):
                # if form is valid and some fields have changed
                # two stages here to set default fields
                with reversion.create_revision():
                    obj = form.save(commit=False)
                    obj.editor = request.user
                    obj.added = timezone.now()
                    obj.save()
        return redirect(w)
    else:
        return render(request, 'lexicon/word_edit.html', {
            'word': w, 'formset': formset
        })
