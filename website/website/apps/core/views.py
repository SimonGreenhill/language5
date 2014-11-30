from django.db.models import Count
from django.conf import settings
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import DetailView, TemplateView
from django.core.urlresolvers import reverse
from django.core.paginator import EmptyPage, PageNotAnInteger

from website.apps.core.models import Family, Language, AlternateName, Source

from django_tables2 import SingleTableView, RequestConfig
from website.apps.core.tables import LanguageIndexTable, SourceIndexTable, FamilyIndexTable
from website.apps.lexicon.tables import LanguageLexiconTable, SourceLexiconTable
from website.apps.lexicon.tables import LanguageLexiconEditTable, SourceLexiconEditTable

class RobotsTxt(TemplateView):
    """simple robots.txt implementation"""
    template_name = "robots.txt"
    content_type = "text/plain"
    

class LanguageIndex(SingleTableView):
    """Language Index"""
    model = Language
    template_name = 'core/language_index.html'
    table_class = LanguageIndexTable
    table_pagination = {"per_page": 50}
    
    def get_queryset(self):
        qset = Language.objects.all()
        if 'subset' in self.request.GET:
            qset = qset.filter(language__istartswith=self.request.GET['subset'])
        if 'website.apps.lexicon' in settings.INSTALLED_APPS:
            qset = qset.annotate(count=Count('lexicon')).all()
        return qset
    
    def get_context_data(self, **kwargs):
        context = super(LanguageIndex, self).get_context_data(**kwargs)
        if 'subset' in self.request.GET:
            context['subset'] = self.request.GET['subset']
        else:
            context['subset'] = None
        context['subsets'] = [_ for _ in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
        return context
    
    
class SourceIndex(SingleTableView):
    """Source Index"""
    model = Source
    template_name = 'core/source_index.html'
    table_class = SourceIndexTable
    table_pagination = {"per_page": 50}
    
    def get_queryset(self):
        qset = Source.objects.all()
        if 'subset' in self.request.GET:
            qset = qset.filter(author__istartswith=self.request.GET['subset'])
        if 'website.apps.lexicon' in settings.INSTALLED_APPS:
            return qset.annotate(count=Count('lexicon')).all()
        return qset

    def get_context_data(self, **kwargs):
        context = super(SourceIndex, self).get_context_data(**kwargs)
        if 'subset' in self.request.GET:
            context['subset'] = self.request.GET['subset']
        else:
            context['subset'] = None
        context['subsets'] = [_ for _ in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
        return context


class FamilyIndex(SingleTableView):
    """Family Index"""
    model = Family
    template_name = 'core/family_index.html'
    table_class = FamilyIndexTable
    table_pagination = {"per_page": 50}
    
    def get_queryset(self):
        qset = Family.objects.annotate(count=Count('language'))
        if 'subset' in self.request.GET:
            qset = qset.filter(family__istartswith=self.request.GET['subset'])
        return qset

    def get_context_data(self, **kwargs):
        context = super(FamilyIndex, self).get_context_data(**kwargs)
        if 'subset' in self.request.GET:
            context['subset'] = self.request.GET['subset']
        else:
            context['subset'] = None
        context['subsets'] = [_ for _ in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
        return context


class SourceDetail(DetailView):
    """Source Detail"""
    model = Source
    template_name = 'core/source_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super(SourceDetail, self).get_context_data(**kwargs)
        context['attachments'] = kwargs['object'].attachment_set.all()
        if 'website.apps.lexicon' in settings.INSTALLED_APPS:
            
            qset = kwargs['object'].lexicon_set.select_related().all()
            if self.request.user.is_authenticated():
                context['lexicon_table'] = SourceLexiconEditTable(qset)
            else:
                context['lexicon_table'] = SourceLexiconTable(qset)
            
            RequestConfig(self.request).configure(context['lexicon_table'])
            
            try:
                context['lexicon_table'].paginate(page=self.request.GET.get('page', 1), per_page=50)
            except EmptyPage: # 404 on a empty page
                raise Http404
            except PageNotAnInteger: # 404 on invalid page number
                raise Http404
        
        return context
    

class FamilyDetail(DetailView):
    """Family Detail"""
    model = Family
    template_name = 'core/family_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super(FamilyDetail, self).get_context_data(**kwargs)
        context['languages'] = LanguageIndexTable(
                kwargs['object'].language_set.all(
                    ).annotate(count=Count('lexicon'))
        
        )
        RequestConfig(self.request).configure(context['languages'])
        return context


def language_detail(request, language):
    """
    Show Language Details
    
    Uses a slug to lookup. If the slug is the primary one in the languages table,
        then the details page will be shown
    If nothing is found in the languages table, then the AlternateNames table is 
        checked for a match. If found, then this view will redirect to the canonical slug.
    """
    # if we find the language slug, then render the language detail page.
    try:
        my_lang = Language.objects.get(slug=language)
        out = {
            'language': my_lang,
            'alternatenames': my_lang.alternatename_set.all(),
            'links': my_lang.link_set.all(),
            'attachments': my_lang.attachment_set.all(),
        }
        
        # sources used 
        source_ids = [_['source_id'] for _ in my_lang.lexicon_set.values('source_id').distinct().all()]
        out['sources_used'] = Source.objects.filter(pk__in=source_ids)
        
        # load lexicon if installed.
        if 'website.apps.lexicon' in settings.INSTALLED_APPS:
            qset = my_lang.lexicon_set.select_related().all()
            if request.user.is_authenticated():
                out['lexicon_table'] = LanguageLexiconEditTable(qset)
            else:
                out['lexicon_table'] = LanguageLexiconTable(qset)
            
            RequestConfig(request).configure(out['lexicon_table'])
            
            try:
                out['lexicon_table'].paginate(page=request.GET.get('page', 1), per_page=50)
            except EmptyPage: # 404 on a empty page
                raise Http404
            except PageNotAnInteger: # 404 on invalid page number
                raise Http404
        
        # load pronouns
        if 'website.apps.pronouns' in settings.INSTALLED_APPS:
            from website.apps.pronouns.models import Paradigm, Pronoun
            from website.apps.pronouns.tools import add_pronoun_table
            try: 
                out['pronoun'] = Paradigm.objects.filter(language=my_lang)[0]
                out['pronoun_rows'] =  add_pronoun_table(out['pronoun'].pronoun_set.all())
            except IndexError: # no paradigm
                pass
            
        return render(request, 'core/language_detail.html', out)
    except Language.DoesNotExist:
        pass
    
    # If we can find an alternate name, redirect it.
    try:
        return redirect(AlternateName.objects.get(slug=language).language, permanent=True)
    except AlternateName.DoesNotExist:
        pass
    # fail. Doesn't exist so pop out a 404
    raise Http404
        
    
def iso_lookup(request, iso):
    """
    ISO Code Lookup
    
    If there is ONE iso code found, then the view will redirect to the correct
        details page.
        
    If there are > 1 found, then the view will list them.
    """
    languages = Language.objects.all().filter(isocode=iso)
    if len(languages) == 1:
        return redirect(languages[0], permanent=True)
    elif len(languages) > 1:
        return render(request, 'core/language_index.html', 
                                    {'table': LanguageIndexTable(languages),
                                     'message': "Multiple Languages found for ISO code %s" % iso, 
                                    })
    else:
        raise Http404
        



