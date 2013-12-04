from django.http import Http404
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.db.models import Q, Count

from website.apps.core.models import Family, Language, Source
from website.apps.pronouns.models import Paradigm, Pronoun, Relationship, Rule
from website.apps.pronouns.tables import ParadigmIndexTable
from website.apps.pronouns.tables import PronounTable
from website.apps.pronouns.tables import PronounRelationshipTable

from website.apps.pronouns.forms import CopyForm, ParadigmForm, RelationshipFormSet, RuleForm
from website.apps.pronouns.forms import pronoun_formsets_are_valid
from website.apps.pronouns.forms import create_pronoun_formset
from website.apps.pronouns.forms import save_pronoun_formset
from website.apps.pronouns.forms import sort_formset


from website.apps.pronouns.tools import add_pronoun_table, copy_paradigm
from website.apps.pronouns.tools import find_identicals, extract_rule

from django_tables2 import SingleTableView

import reversion


class Index(SingleTableView):
    """Index"""
    model = Paradigm
    template_name = 'pronouns/index.html'
    table_class = ParadigmIndexTable
    table_pagination = {"per_page": 50}
    order_by_field = 'language'
    
    def get_queryset(self):
        return Paradigm.objects.select_related().all()



def detail(request, paradigm_id):
    try:
        p = Paradigm.objects.select_related().get(pk=paradigm_id)
        ptable = p.pronoun_set.prefetch_related("entries", "pronountype").all()
        out = {
            'paradigm': p,
            'language': p.language,
            'source': p.source,
            'pronoun_rows': add_pronoun_table(ptable),
            'relationship_table': None
        }
        relationships = p.relationship_set.select_related().all()
        if len(relationships) > 0:
            out['relationship_table'] = PronounRelationshipTable(relationships)
        
        return render(request, 'pronouns/detail.html', out)
    except Paradigm.DoesNotExist:
        raise Http404 # fail. Doesn't exist so pop out a 404
        

@login_required()
@reversion.create_revision()
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
@reversion.create_revision()
def edit(request, paradigm_id):
    p = get_object_or_404(Paradigm, pk=paradigm_id)
    paradigm_form = ParadigmForm(request.POST or None, instance=p, prefix='pdm')
    pronoun_form = create_pronoun_formset(p, request.POST or None)
    
    # save if valid.
    if pronoun_formsets_are_valid(pronoun_form) and paradigm_form.is_valid():
        p = paradigm_form.save(commit=False)
        p.editor = request.user
        p.save()
        for pronoun, formset in pronoun_form:
            saved = save_pronoun_formset(p, pronoun, formset, request.user)
        return redirect('pronouns:detail', p.id)
        
    # the initial view and the error view
    return render_to_response('pronouns/edit.html', {
        'paradigm': p,
        'paradigm_form': paradigm_form,
        'pronouns': sort_formset(pronoun_form),
    }, context_instance=RequestContext(request))



@login_required()
@reversion.create_revision()
def edit_relationships(request, paradigm_id):
    p = get_object_or_404(Paradigm, pk=paradigm_id)
    relationship_form = RelationshipFormSet(request.POST or None, instance=p)
    
    def _fix_relationship_form(relationship_form):
        # Yuck - filter pronouns to match the given paradigm.
        #    -> must be a better way to do this!
        q = Pronoun.objects.all().filter(paradigm=p)
        q = q.annotate(entry_count=Count('entries')).exclude(entry_count=0)
        q = q.select_related()
        
        for f in relationship_form.forms:
            f.fields['pronoun1'].queryset = q
            f.fields['pronoun2'].queryset = q
        return relationship_form
        
    relationship_form = _fix_relationship_form(relationship_form)
    
    if relationship_form.is_valid():
        instances = relationship_form.save(commit=False)
        for obj in instances:
            obj.editor = request.user
            obj.save()
        return redirect('pronouns:detail', p.id)
    
    ptable = p.pronoun_set.prefetch_related("entries", "pronountype").all()
    
    return render_to_response('pronouns/edit_relationships.html', {
        'paradigm': p,
        'language': p.language,
        'source': p.source,
        'pronoun_rows': add_pronoun_table(ptable),
        'relationships': relationship_form,
        'rule_form': RuleForm(),
        'applied_rules': p.rule_set.all(),
    }, context_instance=RequestContext(request))


@login_required()
@reversion.create_revision()
def process_rule(request, paradigm_id):
    p = get_object_or_404(Paradigm, pk=paradigm_id)
    # do we have do_identicals? 
    if 'process_identicals' in request.POST:
        # 1. process form
        members = find_identicals(p)
        
        # 2. implement rule
        if len(members) > 0:
            # 3. save rule to rule table.
            rule = Rule.objects.create(
                paradigm = p,
                rule="Identical Entries set to Total Syncretism",
                editor=request.user
            )
            for m1, m2 in members:
                # Ignore anything we've already set
                if not Relationship.objects.has_relationship_between(m1[0], m2[0]):
                    rel = Relationship.objects.create(
                        paradigm = p, 
                        pronoun1_id=m1[0], pronoun2_id=m2[0], 
                        relationship='TS',
                        editor=request.user
                    )
                    rule.relationships.add(rel)
        
        return redirect('pronouns:edit_relationships', p.id)
        
    elif 'process_rule' in request.POST:
        # 1. process form
        rule_form = RuleForm(request.POST or None)
        if rule_form.is_valid():
            # 2. implement rule
            try:
                rule = extract_rule(ruleform.clean())
            except ValueError:
                # form is broken - go away.
                return redirect('pronouns:edit_relationships', p.id)
                
            # members = process_rule(rule, p.pronoun_set.all())
            
            # 3. save rule to rule table.
            # rule = Rule.objects.create(
            #     paradigm = p,
            #     rule="Identical Entries set to Total Syncretism",
            #     editor=request.user
            # )
            # for p1, p2 in members:
            #     # Ignore anything we've already set
            #     if Relationship.objects.has_relationship_between(p1, p2) == False:
            #         rel = Relationship.objects.create(
            #             paradigm = p, pronoun1=p1, pronoun2=p2, relationship='TS',
            #             editor=request.user
            #         )
            #         rule.relationships.add(rel)
        
        # Note: Invalid forms are IGNORED
        return redirect('pronouns:edit_relationships', p.id)
    else:
        return redirect('pronouns:detail', p.id)
        


@login_required()
@reversion.create_revision()
def copy(request, paradigm_id):
    """Copies a Paradigm"""
    p = get_object_or_404(Paradigm, pk=paradigm_id)
    paradigm_form = ParadigmForm(request.POST or None, instance=p, prefix='pdm')
    copy_form = CopyForm(request.POST or None, prefix='copy')
    
    # save if valid.
    if copy_form.is_valid() and paradigm_form.is_valid():
        # construct a temporary paradigm to validate, we do NOT
        # want to update the original paradigm `p` with the 
        # changed form data, so this is just for holding and
        # validating the incoming form values.
        temp_p = paradigm_form.save(commit=False)
        # copy the old paradigm to the temporary paradigm language
        new_p = copy_paradigm(p, temp_p.language)
        # update details of new paradigm from temporary paradigm
        new_p.editor = request.user
        new_p.comment = temp_p.comment
        new_p.source = temp_p.source
        new_p.analect = temp_p.analect
        new_p.save()
        return redirect('pronouns:detail', new_p.id)
        
    # the initial view and the error view
    return render_to_response('pronouns/copy.html', {
        'paradigm': p,
        'paradigm_form': paradigm_form,
        'copy_form': copy_form,
    }, context_instance=RequestContext(request))

