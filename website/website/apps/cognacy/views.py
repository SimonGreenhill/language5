from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.db import transaction
from django.db.models import Max, Q, Count
from django.shortcuts import get_object_or_404, Http404, render_to_response, redirect
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django_tables2 import SingleTableView, RequestConfig

from reversion import revisions as reversion

from website.apps.core.models import Source
from website.apps.lexicon.models import Word, Lexicon, CognateSet, Cognate, CognateNote
from website.apps.cognacy.forms import DoCognateForm, MergeCognateForm, CognateNoteForm, get_clades
from website.apps.cognacy.tables import CognateSourceIndexTable, CognateSourceDetailTable
from website.apps.cognacy.tables import CognacyTable, CognateSetDetailTable 

from website.apps.cognacy.utils import get_missing_cogids


class CognateSourceIndex(SingleTableView):
    """Cognate Index By Source"""
    model = Source
    template_name = 'cognacy/index.html'
    table_class = CognateSourceIndexTable
    table_pagination = {"per_page": 100}
    
    def get_queryset(self):
        return Source.objects.all().annotate(count=Count('cognate')).filter(count__gt=0)
    

class CognateSourceDetail(DetailView):
    """Cognate Index By Source"""
    model = Source
    template_name = 'cognacy/detail.html'
    table_pagination = {"per_page": 50}
    
    def get_context_data(self, **kwargs):
        context = super(CognateSourceDetail, self).get_context_data(**kwargs)
        qset = []
        for o in kwargs['object'].cognate_set.select_related().all():
            o.language = o.lexicon.language
            o.word = o.lexicon.word
            qset.append(o)
        context['lexicon'] = CognateSourceDetailTable(qset)
        RequestConfig(self.request).configure(context['lexicon'])
            
        try:
            context['lexicon'].paginate(page=self.request.GET.get('page', 1), per_page=50)
        except EmptyPage: # 404 on a empty page
            raise Http404
        except PageNotAnInteger: # 404 on invalid page number
            raise Http404
        
        context['type'] = 'Source'
        return context


class CognateSetDetail(DetailView):
    """Cognate Set Detail"""
    model = CognateSet
    template_name = 'cognacy/detail.html'
    table_pagination = {"per_page": 100}
    
    def get_context_data(self, **kwargs):
        context = super(CognateSetDetail, self).get_context_data(**kwargs)
        qset = []   # yuck
        for o in kwargs['object'].lexicon.select_related('language', 'word', 'source').all():
            o.classification = o.language.classification
            qset.append(o)
        
        context['lexicon'] = CognateSetDetailTable(qset)
        RequestConfig(self.request).configure(context['lexicon'])
        
        try:
            context['lexicon'].paginate(page=self.request.GET.get('page', 1), per_page=50)
        except EmptyPage: # 404 on a empty page
            raise Http404
        except PageNotAnInteger: # 404 on invalid page number
            raise Http404
        # get any notes for this cognate set.
        context['notes'] = CognateNote.objects.filter(cognateset=kwargs['object'])
        context['type'] = 'CognateSet'
        return context

    @method_decorator(login_required) # ensure logged in
    def dispatch(self, *args, **kwargs):
        return super(CognateSetDetail, self).dispatch(*args, **kwargs)


@login_required()
def do_index(request):
    """Do cognacy index to help select subsets"""
    form = DoCognateForm(request.POST or None, clades=get_clades())
    if request.POST and form.is_valid():
        url = reverse('cognacy:do', kwargs={
            'word': form.cleaned_data['word'].slug, 
            'clade': form.cleaned_data['clade']
        })
        return redirect(url)
    return render_to_response('cognacy/do_index.html', {'form': form},
        context_instance=RequestContext(request)
    )


@login_required()
def do(request, word, clade=None):
    """Do cognacy"""
    w = get_object_or_404(Word, slug=word)
    lex_ids, entries = [], []
    lexica = w.lexicon_set.all()
    if clade:
        lexica = lexica.filter(language__classification__startswith=clade)
    
    for e in lexica.select_related('source', 'word', 'language'):
        lex_ids.append(e.id)
        entries.append(e)
    
    # save us from one query for each cognateset -- select_related doesn't help us here so
    # we do a rather ungainly merge.
    # 1. get a list of (lexicon.id, cognateset.id)
    queryset = Cognate.objects.filter(lexicon_id__in=lex_ids).select_related('lexicon', 'cognateset', 'cognateset__source')
    cogs = [(c.lexicon_id, c.cognateset_id, c.cognateset) for c in queryset]
    # 2. get notes
    notes = CognateNote.objects.filter(Q(word=w) | Q(cognateset__in=[c[2] for c in cogs]))
    
    # 3. go through entries and attach a list of cognateset ids if needed, else empty list
    entries_and_cogs = []
    inplay = {}
    for e in entries:
        e.cognacy = [c[1] for c in cogs if c[0] == e.id]
        e.edit = True  # dummy value so django-tables2 passes to render_edit()
        e.classification = e.language.classification
        entries_and_cogs.append(e)
        
        cogobjs = [_[2] for _ in cogs if _[1] in e.cognacy]
        for o in cogobjs:
            inplay[o] = inplay.get(o, set())
            inplay[o].add(e.entry)
    
    inplay = dict([(k, ", ".join(sorted(v)[0:20])) for (k, v) in inplay.items()])
    inplay = sorted([(k.id, k, v) for (k, v) in inplay.items()])
    inplay = [(_[1], _[2]) for _ in inplay]
    
    form = DoCognateForm(initial={'word': w.id, 'clade': clade}, is_hidden=True, clades=get_clades())
    
    
    CSQ = CognateSet.cache_all_method.filter(id__in=[c[1] for c in cogs]).order_by('id')
    mergeform = MergeCognateForm(request.POST or None, prefix='merge', queryset=CSQ)
    commentform = CognateNoteForm(request.POST or None, prefix='comment', 
        queryset=CSQ, initial = {'word': w,}
    )
    
    table = CognacyTable(entries_and_cogs)
    RequestConfig(request, paginate=False).configure(table)
    
    return render_to_response('cognacy/do_detail.html',
                              {
                                  'word': w, 'clade': clade, 'lexicon': table,
                                  'inplay': inplay, 'form': form,
                                  'mergeform': mergeform,
                                  'next_cognates': get_missing_cogids(limit=10),
                                  'notes': notes,
                                  'commentform': commentform,
                              },
                              context_instance=RequestContext(request))


@login_required()
def save(request, word, clade=None):
    form = DoCognateForm(request.POST or None, clades=get_clades())
    commentform = CognateNoteForm(request.POST or None, prefix='comment',
        queryset=CognateSet.objects.all()
    )
    
    if request.POST and commentform.is_valid():
        CognateNote.objects.create(
            word=commentform.cleaned_data['word'],
            cognateset=commentform.cleaned_data['cogset'],
            note=commentform.cleaned_data['comment'],
            editor=request.user,
        )
    
    if request.POST and form.is_valid():
        word = form.cleaned_data['word']
        clade = form.cleaned_data['clade']
        # collect lexicon ids and actions
        # 1. get anything (lex_id, value) that is a cognacy field and isn't empty
        changes = [
            (k[2:], v) for (k, v) in request.POST.items() if k.startswith('c-') and v != u''
        ]
        
        # check that we've got valid lexical ids
        # Any exceptions here should only be due to tampering -- cause a 500 error.
        try:
            changes = [(int(k), v) for (k, v) in changes]
        except ValueError:
            raise ValueError("Form tampering!")
        
        # pull out subsets of actions
        commands = [
            (k, v) for (k, v) in changes if v.startswith("!")
        ]
        additions = [
            (k, v) for (k, v) in changes if v.startswith('-') == False and v.startswith("!") == False
        ]
        deletions = [
            (k, v[1:]) for (k, v) in changes if v.startswith('-') and v.startswith("!") == False
        ]
        
        
        # 1. Special commands
        for lex_id, command in commands:
            L = Lexicon.objects.get(pk=lex_id)
            if command == '!DELETE':
                messages.add_message(request, messages.WARNING, 
                    'Warning: DELETED lexicon %r' % L, 
                    extra_tags='warning'
                )
                with reversion.create_revision():
                    L.delete()
                    reversion.set_user(request.user)
                    reversion.set_comment("Deleted item")
                    
        # 2. Cognate Additions
        for lex_id, cogset in additions:
            L = Lexicon.objects.get(pk=lex_id)
            
            try:
                cog = CognateSet.objects.get(pk=int(cogset))
            except ValueError:  # non numeric input. Can't be a PK
                messages.add_message(request, messages.ERROR, 
                    'ERROR %r for lexicon %d is not a number' % (cogset, lex_id), 
                    extra_tags='error'
                )
                continue
            except CognateSet.DoesNotExist:  # doesn't exist -- create
                with reversion.create_revision():
                    cog = CognateSet.objects.create(
                        pk=int(cogset),
                        protoform = "",
                        gloss = "",
                        editor=request.user
                    )
                    cog.save()
                messages.add_message(request, messages.INFO, 
                    'Creating Cognate Set %r' % cog, 
                    extra_tags='success'
                )
            
            # avoid duplicates
            if L not in cog.lexicon.all():
                with reversion.create_revision():
                    Cognate.objects.create(lexicon=L, cognateset=cog, editor=request.user).save()
                messages.add_message(request, messages.INFO, 
                    'Adding %r to cognate set %d' % (L, cog.id), 
                    extra_tags='success'
                )
            else:
                messages.add_message(request, messages.WARNING, 
                    'Warning: %r already in cognate set %d' % (L, cog.id), 
                    extra_tags='warning'
                )
        
        # 3. Cognate Deletions
        for lex_id, cogset in deletions:
            L = Lexicon.objects.get(pk=lex_id)
            cog = None
            
            try:
                cog = CognateSet.objects.get(pk=int(cogset))
            except ValueError:  # non numeric input. Can't be a PK
                messages.add_message(request, messages.ERROR,
                    'ERROR %r for lexicon %d is not a number' % (cogset, lex_id),
                    extra_tags='error'
                )
                continue
            except CognateSet.DoesNotExist:  # doesn't exist -- create
                messages.add_message(request, messages.ERROR,
                    'ERROR CognateSet %r does not exist' % cogset,
                    extra_tags='error'
                )
                continue
                
            members = [_ for _ in L.cognate_set.all() if _.cognateset_id == cog.id]
            for m in members:
                messages.add_message(request, messages.INFO,
                    'Removing %r to cognate set %d' % (L, cog.id),
                    extra_tags='warning'
                )
                with reversion.create_revision():
                    m.delete()
            
            # remove cognateset if it's empty
            if cog.cognate_set.count() == 0:
                messages.add_message(request, messages.INFO,
                    'Removing empty cognate set %r' % cog,
                    extra_tags='warning'
                )
                with reversion.create_revision():
                    cog.delete()
        
        url = reverse('cognacy:do', kwargs={
            'word': form.cleaned_data['word'].slug, 
            'clade': form.cleaned_data['clade']
        })
        return redirect(url)
    return redirect(reverse('cognacy:do_index'))  # go somewhere safe on form tamper.
    


@login_required()
def merge(request, word, clade=None):
    form = MergeCognateForm(request.POST or None,
        prefix='merge', 
        queryset=CognateSet.objects.all()  # needed as we've explicitly set None in the form.
    )
    
    if request.POST and form.is_valid():
        old = form.cleaned_data['old']
        new = form.cleaned_data['new']
        
        messages.add_message(request, messages.INFO,
            'Moving cognate set %r to %r' % (old, new),
            extra_tags='warning'
        )
        # get the lexical items already in this cognateset
        already = [lex for lex in new.lexicon.all()]
        
        with reversion.create_revision():
            for cog in old.cognate_set.all():
                if cog.lexicon in already:
                    cog.delete()  # already got it in this cognate set. Delete the cognate
                else:
                    cog.cognateset = new
                    cog.save()
            old.delete()
    url = reverse('cognacy:do', kwargs={'word': word, 'clade': clade})
    return redirect(url)
