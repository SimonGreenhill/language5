from django.db.models import Count
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404, redirect
from core.models import Family, Language, AlternateNames

def language_index(request):
    "Language Index"
    
    # handle table sorting.
    order = request.GET.get('order', 'language')
    if order not in ['language', 'isocode', 'family']:
        order = 'language'
    
    languages = Language.objects.all().select_related('family__family', 'family__slug')
    languages = languages.defer('information', 'classification')
    languages = languages.order_by(order)
    return render_to_response('language/index.html', {'languages': languages})

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
            'alternatenames': my_lang.alternatenames_set.all(),
            'links': my_lang.links_set.all(),
        }
        return render_to_response('language/detail.html', out)
    except Language.DoesNotExist:
        pass
    
    # If we can find an alternate name, redirect it.
    try:
        return redirect(AlternateNames.objects.get(slug=language).language, permanent=True)
    except AlternateNames.DoesNotExist:
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
        return render_to_response('language/index.html', {'languages': languages})
    else:
        raise Http404
        



def family_index(request):
    """Family Index"""
    # sort out ordering
    order = request.GET.get('order', 'family')
    if order not in ['family', 'count']:
        order = 'family'
    families = Family.objects.annotate(count=Count('language')).order_by(order)
    return render_to_response('family/index.html', {'families': families})


def family_detail(request, family):
    """Show Family Details"""
    # sort out ordering
    order = request.GET.get('order', 'name')
    if order not in ['language', 'count', 'isocode']:
        order = 'language'
    
    f = get_object_or_404(Family, slug=family)
    l = f.language_set.all().order_by(order)
    return render_to_response('family/detail.html', {'family': f, 'languages':l})

