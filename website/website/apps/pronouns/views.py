from django.http import Http404
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.forms.formsets import modelformset_factory

from website.apps.core.models import Family, Language, Source
from website.apps.pronouns.models import Paradigm
from website.apps.pronouns.tables import ParadigmIndexTable, PronounTable

from website.apps.pronouns.forms import ParadigmForm, RelationshipFormSet
from website.apps.pronouns.forms import SimplePronounForm, AdvancedPronounFormSet

from django_tables2 import SingleTableView

from website.apps.pronouns.tools import generate_pronoun_formsets

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
            'pronoun_table': PronounTable(p.pronoun_set.all()),
            #'relationships': p.relationship_set.all(),
        }
        return render(request, 'pronouns/view.html', out)
    except Paradigm.DoesNotExist:
        raise Http404 # fail. Doesn't exist so pop out a 404
        

@login_required()
def edit(request, paradigm_id):
    p = get_object_or_404(Paradigm, pk=paradigm_id)
    
    # process form
    if request.method == 'POST':
        paradigm_form = ParadigmForm(request.POST, instance=p)
        SimplePronounFormSet = modelformset_factory(SimplePronounForm, extra=0)
        pronoun_formset = SimplePronounFormSet(request.POST, prefix="pron")
        relationship_formset = RelationshipFormSet(request.POST, prefix="rel")
        
        #print 'PARADIGM_FORM:', paradigm_form.is_valid()
        #print 'PRONOUN_FORMSET:', pronoun_formset.is_valid()
        #print 'RELATIONSHIP_FORMSET:', relationship_formset.is_valid()
        
        if paradigm_form.is_valid() and pronoun_formset.is_valid() and relationship_formset.is_valid():
            
            # PARADIGM FORM
            p = paradigm_form.save(commit=True)
            
            # PRONOUNS
            for form in pronoun_formset:
                if form.is_valid() and len(form.changed_data):
                    obj = form.save(commit=False)
                    obj.editor = request.user
                    obj.paradigm = p
                    obj.save()
            
            # RELATIONSHIPS
            for form in relationship_formset:
                if form.is_valid() and len(form.changed_data):
                    obj = form.save(commit=False)
                    obj.editor = request.user
                    obj.save()
            
            return redirect('pronouns:detail', p.id)
    else:
        paradigm_form = ParadigmForm(instance=p)
        pronoun_set = p.pronoun_set.all()
        if len(pronoun_set) > 0:
            SimplePronounFormSet = modelformset_factory(SimplePronounForm, extra=0)
            pronoun_formset = SimplePronounFormSet(initial=[i for i in p.pronoun_set.all()], prefix="pron")
        else:
            SimplePronounFormSet = modelformset_factory(SimplePronounForm, extra=1)
            pronoun_formset = SimplePronounFormSet(prefix="pron")
            
        relationship_formset = RelationshipFormSet(initial=p.relationship_set.all(), prefix="rel")
        
    # the initial view and the error view
    return render_to_response('pronouns/edit.html', {
        'paradigm': p,
        'paradigm_form': paradigm_form,
        'pronoun_formset': pronoun_formset,
        'relationship_formset': relationship_formset,
    }, context_instance=RequestContext(request))





@login_required()
def edit_advanced(request, paradigm_id):
    p = get_object_or_404(Paradigm, pk=paradigm_id)

    # process form
    if request.method == 'POST':
        pronoun_formsets = AdvancedPronounFormSet(request.POST)
        relationship_formset = RelationshipFormSet(request.POST)
        
        raise NotImplementedError("Not yet implemented.")
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
        paradigm_form = ParadigmForm(instance=p)
        pronoun_formsets = generate_pronoun_formsets(p)
        relationship_formset = RelationshipFormSet(initial=p.relationship_set.all())

    # the initial view and the error view
    return render_to_response('pronouns/edit_advanced.html', {
        'relationship_formset': relationship_formset,
        'paradigm_form': paradigm_form,
        'pronoun_formsets': pronoun_formsets,
        'paradigm': p,
    }, context_instance=RequestContext(request))
