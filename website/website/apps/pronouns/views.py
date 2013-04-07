from django.http import Http404
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.utils.functional import curry

from website.apps.core.models import Family, Language, Source
from website.apps.pronouns.models import Paradigm, Pronoun, Relationship
from website.apps.pronouns.tables import ParadigmIndexTable, PronounTable, PronounRelationshipTable

from website.apps.pronouns.forms import ParadigmForm#, RelationshipFormSet
from website.apps.pronouns.forms import PronounFormSet
from website.apps.pronouns.forms import PronounParadigmForm

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
            'pronoun_table': PronounTable(p.pronoun_set.all()),
            'relationship_table': PronounRelationshipTable(p.relationship_set.all())
        }
        return render(request, 'pronouns/view.html', out)
    except Paradigm.DoesNotExist:
        raise Http404 # fail. Doesn't exist so pop out a 404
        

@login_required()
def add(request):
    paradigm_form = ParadigmForm(request.POST or None)
    if paradigm_form.is_valid():
        p = paradigm_form.save(commit=False)
        p.editor = request.user
        p.save()
        return redirect('pronouns:edit', p.id)
    
    return render_to_response('pronouns/add.html', {
        'paradigm_form': paradigm_form,
    }, context_instance=RequestContext(request))


@login_required()
def edit(request, paradigm_id):
    p = get_object_or_404(Paradigm, pk=paradigm_id)
    
    pronoun_form = PronounFormSet(request.POST or None, instance=p)
    
    if pronoun_form.is_valid():
        instances = pronoun_form.save(commit=False)
        for obj in instances:
            obj.editor = request.user
            obj.paradigm = p
            obj.save()
        return redirect('pronouns:detail', p.id)
        
        
    # ADD ROWS::: --> REFACTOR
    def repr_row_instance(p):
        return "%s %s %s" % (p.get_person_display(), p.get_number_display(), p.get_gender_display())

    rows = {}
    for form in pronoun_form:
        row = repr_row_instance(form.instance)
        rows[row] = rows.get(row, 
            dict(zip([x[0] for x in Pronoun.ALIGNMENT_CHOICES], [None for x in Pronoun.ALIGNMENT_CHOICES]))
        )
        rows[row][form.instance.alignment] = form

    pronoun_form.pronoun_rows = []
    # Sort
    for row in Pronoun._generate_all_combinations():
        wanted_label = "%s %s %s" % (row['person'][1], row['number'][1], row['gender'][1]) 
        found_row = False
        for label in rows:
            if wanted_label == label:
                pronoun_form.pronoun_rows.append((label, rows[label]))
                found_row = True
        assert found_row, "Unable to find expected row for Paradigm: %s" % label
    # ::: <<- REFACTOR


    
    # the initial view and the error view
    return render_to_response('pronouns/edit.html', {
        'paradigm': p,
        'pronouns': pronoun_form,
    }, context_instance=RequestContext(request))



# ----------------------------------------------------------- #
# @login_required()
# def edit(request, paradigm_id):
#     p = get_object_or_404(Paradigm, pk=paradigm_id)
#     pronoun_formset = AdvancedPronounFormSet(request.POST or None)
#     if pronoun_formset.is_valid():
#         instances = pronoun_formset.save(commit=False)
#         for obj in instances:
#             obj.editor = request.user
#             obj.paradigm = p
#             obj.save()
#         return redirect('pronouns:detail', p.id)
#     
#     # the initial view and the error view
#     return render_to_response('pronouns/edit.html', {
#         'paradigm': p,
#         'pronouns': pronoun_formset,
#     }, context_instance=RequestContext(request))





@login_required()
def edit_advanced(request, paradigm_id):
    pass
#     p = get_object_or_404(Paradigm, pk=paradigm_id)
# 
#     # process form
#     if request.method == 'POST':
#         pronoun_formsets = AdvancedPronounFormSet(request.POST)
#         relationship_formset = RelationshipFormSet(request.POST)
#         
#         raise NotImplementedError("Not yet implemented.")
#         # RELATIONSHIPS
#         # if relationship_formset.is_valid():
#         #     completed = []
#         #     for form in relationship_formset:
#         #         if form.is_valid() and len(form.changed_data):
#         #             # if form is valid and some fields have changed
#         #             # two stages here to set default fields
#         #             obj = form.save(commit=False)
#         #             obj.editor = request.user
#         #             obj.save()
#         #             completed.append(obj)
# 
#         # ONLY redirect if forms are ok...
#         # the initial view and the error view
#         # return render_to_response('pronouns/edit.html', {
#         #     'paradigm_form': paradigm_form,
#         #     'language_form': language_form,
#         #     'source_form': source_form,
#         #     'relationship_formset': relationship_formset,
#         # }, context_instance=RequestContext(request))
#     else:
#         paradigm_form = ParadigmForm(instance=p)
#         pronoun_formsets = generate_pronoun_formsets(p)
#         relationship_formset = RelationshipFormSet(initial=p.relationship_set.all())
# 
#     # the initial view and the error view
#     return render_to_response('pronouns/edit_advanced.html', {
#         'relationship_formset': relationship_formset,
#         'paradigm_form': paradigm_form,
#         'pronoun_formsets': pronoun_formsets,
#         'paradigm': p,
#     }, context_instance=RequestContext(request))
