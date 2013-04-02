from django.http import Http404
from django.shortcuts import render, redirect

from website.apps.core.models import Family, Language, Source
from website.apps.pronouns.models import Paradigm
from website.apps.pronouns.tables import ParadigmIndexTable

from django_tables2 import SingleTableView


class Index(SingleTableView):
    """Index"""
    model = Paradigm
    template_name = 'pronouns/index.html'
    table_class = ParadigmIndexTable
    table_pagination = {"per_page": 50}

def detail(request, paradigm_id):
    try:
        p = Paradigm.objects.get(pk=paradigm_id)
        out = {
            'paradigm': p,
            'language': p.language,
            'source': p.source,
            'relationships': p.relationship_set()
        }
        return render(request, 'pronouns/view.html', out)
    except Paradigm.DoesNotExist:
        raise Http404 # fail. Doesn't exist so pop out a 404
        
def add(request):
    pass

def edit(request, paradigm_id):
    """Edit Paradigm Details"""
    try:
        p = Paradigm.objects.get(pk=paradigm_id)
        out = {
            'paradigm': p,
            'language': p.language,
            'source': p.source,
            'relationships': p.relationship_set()
        }
        return render(request, 'pronouns/edit.html', out)
    except Paradigm.DoesNotExist:
        raise Http404 # fail. Doesn't exist so pop out a 404
        
