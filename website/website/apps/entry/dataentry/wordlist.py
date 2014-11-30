from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from django import forms
from django.forms.formsets import formset_factory

from website.apps.core.models import Language, Source
from website.apps.lexicon.models import Lexicon, Word
from website.apps.entry.dataentry.generic import process_post_and_save, GenericFormset

@login_required()
def WordlistView(request, task):
    """Data entry task using a wordlist"""
    template_name = "entry/formtemplates/generic.html"
    
    # Load wordlist.
    assert task.wordlist
    words = task.wordlist.words.order_by('wordlistmember__order').all()
    
    # Set up initial data.
    initial = []
    for i, w in enumerate(words, 1):
        initial.append({
            'language': task.language,
            'source': task.source,
            'word': w,
            'order_id': i, # not used by form processing but just to show the number of the item in HTML
        })
    
    # process form
    if request.POST:
        formset = GenericFormset(request.POST, initial=initial)
        if process_post_and_save(request, task, formset):
            return redirect('entry:complete', pk=task.id)
    else:
        formset = GenericFormset(initial=initial)
    
    return render_to_response('entry/detail.html', {
        'task': task,
        'formset': formset,
        'template': template_name,
    }, context_instance=RequestContext(request))

