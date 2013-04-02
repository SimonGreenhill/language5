from django.http import Http404
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.template.defaultfilters import slugify

from website.apps.core.models import Family, Language, Source
from website.apps.pronouns.models import Paradigm
from website.apps.pronouns.tables import ParadigmIndexTable

from website.apps.pronouns.forms import ParadigmForm, RelationshipFormSet
from website.apps.pronouns.forms import LanguageForm, SourceForm

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
        

@login_required()
def add(request):
    # process form
    if request.method == 'POST':
        
        paradigm_form = ParadigmForm(request.POST)
        language_form = LanguageForm(request.POST)
        source_form = SourceForm(request.POST)
        relationship_formset = RelationshipFormSet(request.POST)
        
        lng, src, pdm = None, None, None
        
        # go through each form and validate...
        # LANGUAGE
        if language_form.is_valid():
            lng = language_form.save(commit=False)
            lng.editor = request.user
            lng.slug = slugify(lng.language)
            lng.save()
            language_form = LanguageForm(lng)
        
        # SOURCE
        if source_form.is_valid():
            src = source_form.save(commit=False)
            src.editor = request.user
            src.slug = slugify(" ".join(src.author, src.year))
            src.save()
            source_form = SourceForm(src)
            
        # PARADIGM
        # if paradigm_form.is_valid() and lng is not None and src is not None:
        #     pdm = paradigm_form.save(commit=False)
        #     pdm.language = lng
        #     pdm.source = src
        #     pdm.editor = request.user
        #     pdm.save()
        # 
        # PRONOUNS>>>>>
        
        # RELATIONSHIPS
        # if relationship_formset.is_valid():
        #     completed = []
        #     for form in relationship_formset:
        #         if form.is_valid() and len(form.changed_data):
        #             # if form is valid and some fields have changed
        #             # two stages here to set default fields
        #             obj = form.save(commit=False)
        #             obj.editor = request.user
        #             obj.save()
        #             completed.append(obj)
                    
        # ONLY redirect if forms are ok...
        # the initial view and the error view
        # return render_to_response('pronouns/edit.html', {
        #     'paradigm_form': paradigm_form,
        #     'language_form': language_form,
        #     'source_form': source_form,
        #     'relationship_formset': relationship_formset,
        # }, context_instance=RequestContext(request))
    else:
        # initialise to empty
        paradigm_form = ParadigmForm()
        language_form = LanguageForm()
        source_form = SourceForm()
        relationship_formset = RelationshipFormSet()
        

    # the initial view and the error view
    return render_to_response('pronouns/edit.html', {
        'paradigm_form': paradigm_form,
        'language_form': language_form,
        'source_form': source_form,
        'relationship_formset': relationship_formset,
    }, context_instance=RequestContext(request))
    

    


@login_required()
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
        
