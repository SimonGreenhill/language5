from django.db.models import Count
from django.conf import settings
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import DetailView

from website.apps.core.models import Family, Language, AlternateName, Source

from django_tables2 import SingleTableView
from website.apps.core.tables import LanguageIndexTable, SourceIndexTable, FamilyIndexTable
from website.apps.lexicon.tables import LanguageLexiconTable, SourceLexiconTable

class LanguageIndex(SingleTableView):
    """Language Index"""
    model = Language
    template_name = 'core/language_index.html'
    table_class = LanguageIndexTable
    table_pagination = {"per_page": 50}
    order_by_field = 'language'


class SourceIndex(SingleTableView):
    """Source Index"""
    model = Source
    template_name = 'core/source_index.html'
    table_class = SourceIndexTable
    table_pagination = {"per_page": 50}
    order_by_field = 'slug'


class FamilyIndex(SingleTableView):
    """Family Index"""
    model = Family
    template_name = 'core/family_index.html'
    table_class = FamilyIndexTable
    table_pagination = {"per_page": 50}
    order_by_field = 'family'
    
    def get_queryset(self):
        return Family.objects.annotate(count=Count('language'))


class SourceDetail(DetailView):
    """Source Detail"""
    model = Source
    template_name = 'core/source_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super(SourceDetail, self).get_context_data(**kwargs)
        if 'website.apps.lexicon' in settings.INSTALLED_APPS:
            context['lexicon_table'] = SourceLexiconTable(kwargs['object'].lexicon_set.all())
        return context
    

class FamilyDetail(DetailView):
    """Family Detail"""
    model = Family
    template_name = 'core/family_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super(FamilyDetail, self).get_context_data(**kwargs)
        context['languages'] = LanguageIndexTable(kwargs['object'].language_set.all())
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
        }
        
        # load lexicon if installed.
        if 'website.apps.lexicon' in settings.INSTALLED_APPS:
            out['lexicon_table'] = LanguageLexiconTable(my_lang.lexicon_set.all())
            
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
        

