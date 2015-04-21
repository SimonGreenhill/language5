from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext

from website.apps.lexicon.models import Word
from website.apps.cognacy.forms import DoCognateForm

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
# test - is logged in. 
# test - handle post.



@login_required()
def do(request, word, clade):
    
    w = get_object_or_404(Word, slug=word)
    lex_ids, entries = [], []
    for e in w.lexicon_set.select_related('source', 'word', 'language').all():
        lex_ids.append(e.id)
        entries.append(e)

    # save us from one query for each cognateset -- select_related doesn't help us here so
    # we do a rather ungainly merge.
    from website.apps.lexicon.models import Cognate
    cogs = [(c.lexicon.id, c.cognateset.id) for c in Cognate.objects.filter(id__in=lex_ids)]
    entries_and_cogs = []
    for e in entries:
        e.cognacy = [c[1] for c in cogs if c[0] == e.id]
        entries_and_cogs.append(e)

    inplay = set([c[1] for c in cogs])
    # entries = []
    # inplay = set()
    # for e in w.lexicon_set.select_related('source', 'word', 'language').all():
    #     #
    #     # e.cognacy = set([c.cognateset.id for c in e.cognate_set.all()])
    #     inplay.add(c.cognateset.id)
    #     entries.append(e)

    return render_to_response('lexicon/word_cognacy.html',
                              {'object': w, 
                              #'lexicon': CognacyTable(entries_and_cogs), 'inplay': inplay},
                              },
                              context_instance=RequestContext(request))
