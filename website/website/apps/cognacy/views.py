from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import transaction
from django.db.models import Max
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext

import reversion

from website.apps.lexicon.models import Word, Lexicon, CognateSet, Cognate
from website.apps.cognacy.forms import DoCognateForm
from website.apps.cognacy.tables import CognacyTable


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
    queryset = Cognate.objects.filter(lexicon_id__in=lex_ids).select_related('lexicon')
    cogs = [(c.lexicon_id, c.cognateset_id) for c in queryset]
    # 2. go through entries and attach a list of cognateset ids if needed, else empty list
    entries_and_cogs = []
    inplay = {}
    for e in entries:
        e.cognacy = [c[1] for c in cogs if c[0] == e.id]
        e.edit = True  # dummy value so django-tables2 passes to render_edit()
        entries_and_cogs.append(e)
        
        for cog in e.cognacy:
            inplay[cog] = inplay.get(cog, set())
            inplay[cog].add(e.entry)
        
    try:
        max_id = int(CognateSet.objects.all().aggregate(Max('id'))['id__max'])
    except TypeError:
        max_id = 1
    
    inplay = dict([(k, ", ".join(sorted(v)[0:10])) for (k, v) in inplay.items()])
    
    form = DoCognateForm(initial={'word': w.id, 'clade': clade}, is_hidden=True)
    return render_to_response('cognacy/detail.html',
                              {
                                  'word': w, 'clade': clade,
                                  'lexicon': CognacyTable(entries_and_cogs),
                                  'inplay': inplay,
                                  'form': form,
                                  'next_cognates': range(max_id + 1, max_id + 11),
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
    
