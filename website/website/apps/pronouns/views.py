from django.http import Http404
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.db.models import Count
from django.core.paginator import EmptyPage, PageNotAnInteger

from website.apps.pronouns.models import Paradigm, Pronoun, Relationship, Rule
from website.apps.pronouns.tables import ParadigmIndexTable

from website.apps.pronouns.forms import CopyForm, ParadigmForm
from website.apps.pronouns.forms import pronoun_formsets_are_valid, sort_formset
from website.apps.pronouns.forms import create_pronoun_formset, save_pronoun_formset

from website.apps.pronouns.tools import add_pronoun_table, copy_paradigm

from django_tables2 import SingleTableView, RequestConfig

from reversion import revisions as reversion


class Index(SingleTableView):
    """Index"""
    model = Paradigm
    template_name = 'pronouns/index.html'
    table_class = ParadigmIndexTable
    table_pagination = {"per_page": 50}
    order_by = 'language'
    
    def get_queryset(self):
        return Paradigm.objects.select_related().all()
    
    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
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
        return render(request, 'pronouns/detail.html', out)
    except Paradigm.DoesNotExist:
        raise Http404  # fail. Doesn't exist so pop out a 404
        

@login_required()
@reversion.create_revision()
def add(request):
    paradigm_form = ParadigmForm(request.POST or None)
    if paradigm_form.is_valid():
        p = paradigm_form.save(commit=False)
        p.editor = request.user
        p.save()
        return redirect('pronouns:edit', p.id)
    
    return render(request, 'pronouns/add.html', {
        'paradigm_form': paradigm_form,
    })


@login_required()
@reversion.create_revision()
def edit(request, paradigm_id):
    pdm = get_object_or_404(Paradigm, pk=paradigm_id)
    paradigm_form = ParadigmForm(
        request.POST or None, instance=pdm, prefix='pdm'
    )
    pronoun_form = create_pronoun_formset(pdm, request.POST or None)
    # save if valid.
    if pronoun_formsets_are_valid(pronoun_form) and paradigm_form.is_valid():
        pdm = paradigm_form.save(commit=False)
        pdm.editor = request.user
        pdm.save()
        for pronoun, formset in pronoun_form:
            save_pronoun_formset(pdm, pronoun, formset, request.user)
        return redirect('pronouns:detail', paradigm_id=pdm.id)
        
    # the initial view and the error view
    return render(request, 'pronouns/edit.html', {
        'paradigm': pdm,
        'paradigm_form': paradigm_form,
        'pronouns': sort_formset(pronoun_form),
    })



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
    
    return render(request, 'pronouns/edit_relationships.html', {
        'paradigm': p,
        'language': p.language,
        'source': p.source,
        'pronoun_rows': add_pronoun_table(ptable),
        'relationships': relationship_form,
        'rule_form': RuleForm(),
        'applied_rules': p.rule_set.all(),
    })



@login_required()
@reversion.create_revision()
def copy(request, paradigm_id):
    """Copies a Paradigm"""
    p = get_object_or_404(Paradigm, pk=paradigm_id)
    paradigm_form = ParadigmForm(
        request.POST or None, instance=p, prefix='pdm'
    )
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
    return render(request, 'pronouns/copy.html', {
        'paradigm': p,
        'paradigm_form': paradigm_form,
        'copy_form': copy_form,
    })

