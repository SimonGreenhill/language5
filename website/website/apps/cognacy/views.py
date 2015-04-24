from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import transaction
from django.db.models import Max
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django_tables2 import RequestConfig

import reversion

from website.apps.lexicon.models import Word, Lexicon, CognateSet, Cognate
from website.apps.cognacy.forms import DoCognateForm, MergeCognateForm
from website.apps.cognacy.tables import CognacyTable


def get_missing_cogids(limit=10):
    cogids = CognateSet.objects.all().values_list('id', flat=True)
    # handle no cognate case.
    if len(cogids) == 0:
        return range(1, limit + 1)
    
    # find the maximum cognate id and adding limit to it -- this 
    # means that we can iterate over things happily and always return
    # $limit records
    max_cog_id = max(cogids) + limit
    return [i for i in range(1, max_cog_id + 1) if i not in cogids][0:limit]


@login_required()
def index(request):
    form = DoCognateForm(request.POST or None)
    if request.POST and form.is_valid():
        url = reverse('cognacy:do', kwargs={
            'word': form.cleaned_data['word'].slug, 
            'clade': form.cleaned_data['clade']
        })
        return redirect(url)
    return render_to_response('cognacy/index.html', {'form': form},
        context_instance=RequestContext(request)
    )


@login_required()
def do(request, word, clade=None):
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
    # 2. go through entries and attach a list of cognateset ids if needed, else empty list
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
    
    form = DoCognateForm(initial={'word': w.id, 'clade': clade}, is_hidden=True)
    
    mergeform = MergeCognateForm(
        prefix='merge', 
        queryset=CognateSet.cache_all_method.filter(id__in=[c[1] for c in cogs]).order_by('id')
    )
    
    table = CognacyTable(entries_and_cogs)
    RequestConfig(request, paginate=False).configure(table)
    
    return render_to_response('cognacy/detail.html',
                              {
                                  'word': w, 'clade': clade, 'lexicon': table,
                                  'inplay': inplay, 'form': form,
                                  'mergeform': mergeform,
                                  'next_cognates': get_missing_cogids(limit=10),
                              },
                              context_instance=RequestContext(request))



@login_required()
def save(request, word, clade=None):
    form = DoCognateForm(request.POST or None)
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
        
        # Special commands
        commands = [(k, v) for (k, v) in changes if v.startswith("!")]
        if len(commands):
            "!DELETE"
            import IPython; IPython.embed();
        
        changes = [(k, v) for (k, v) in changes if v.startswith("!") == False]
        # ADDITIONS
        additions = [(k, v) for (k, v) in changes if v.startswith('-') == False]
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
        
        # DELETIONS
        deletions = [(k, v[1:]) for (k, v) in changes if v.startswith('-')]
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
    return redirect(reverse('cognacy:index'))  # go somewhere safe on form tamper.
    


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
