from django.http import Http404
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

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
        pass
        # formset = GenericFormSet(request.POST)
        # 
        # if formset.is_valid():
        #     completed = []
        #     for form in formset:
        #         if form.is_valid() and len(form.changed_data):
        #             # if form is valid and some fields have changed
        #             # two stages here to set default fields
        #             obj = form.save(commit=False)
        #             obj.editor = request.user
        #             obj.save()
        #             completed.append(obj)
        #             
        #     # update task if needed.
        #     if task.completable == True:
        #         task.done = True
        #         task.save()
        #     
        #     return render_to_response('entry/done.html', {
        #         'task': task,
        #         'objects': completed,
        #     }, context_instance=RequestContext(request))
    else:
        return render_to_response('pronouns/edit.html', {
            'paradigm_form': ParadigmForm(),
            'language_form': LanguageForm(),
            'source_form': SourceForm(),
            'relationship_formset': RelationshipFormSet()
            
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
        
