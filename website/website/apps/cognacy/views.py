from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext

from website.apps.lexicon.models import Word, Cognate
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
    for e in entries:
        e.cognacy = [c[1] for c in cogs if c[0] == e.id]
        entries_and_cogs.append(e)
    
    inplay = set([c[1] for c in cogs])

    return render_to_response('cognacy/detail.html',
                              {
                                  'word': w, 
                                  'lexicon': CognacyTable(entries_and_cogs),
                                  'inplay': inplay
                              },
                              context_instance=RequestContext(request))
