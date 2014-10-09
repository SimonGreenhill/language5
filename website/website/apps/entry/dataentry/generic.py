import copy

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from django import forms
from django.forms.formsets import formset_factory

import reversion

from website.apps.core.models import Language, Source
from website.apps.lexicon.models import Lexicon, Word

from website.apps.entry.utils import task_log

class GenericForm(forms.ModelForm):
    language = forms.ModelChoiceField(queryset=Language.cache_all_method.all().order_by('slug'))
    word = forms.ModelChoiceField(queryset=Word.cache_all_method.all().order_by('word'))
    source = forms.ModelChoiceField(queryset=Source.cache_all_method.all().order_by('slug'))
    
    class Meta:
        model = Lexicon
        fields = ['language', 'source', 'word', 'entry', 'annotation']
        widgets = {
            # over-ride Textarea for annotation
            'annotation': forms.widgets.TextInput(
                    attrs={'class': 'input-medium'}),
            
            # and set input size
            'entry': forms.widgets.TextInput(attrs={'class': 'input-medium'}),
            'language': forms.widgets.Select(attrs={'class': 'input-medium'}),
            'source': forms.widgets.Select(attrs={'class': 'input-medium'}),
            'word': forms.widgets.Select(attrs={'class': 'input-medium'}),
        }
    # make sure to set editor, added, and loan if loan_source is specified

GenericFormset = formset_factory(GenericForm, extra=0)


def process_post_and_save(request, task, formset):
    """Extracted common code to process a form."""
    
    if 'refresh' in request.POST:
        task_log(request, task=task, message="Refreshed Task")
    elif 'submit' in request.POST:
        # fill if necessary
        for form in formset.forms:
            if task.language and '%s-language' % form.prefix not in form.data:
                form.data['%s-language' % form.prefix] = task.language.id
            if task.source and '%s-source' % form.prefix not in form.data:
                form.data['%s-source' % form.prefix] = task.source.id
        
        if formset.is_valid():
            completed = []
            for form in formset:
                if form.is_valid() and len(form.changed_data):
                    # if form is valid and some fields have changed
                    # two stages here to set default fields
                    with reversion.create_revision():
                        obj = form.save(commit=False)
                        obj.editor = request.user
                        obj.save()
                        
                    with reversion.create_revision():
                        task.lexicon.add(obj)
                    
                    completed.append(obj)
                    
            task_log(request, task=task, message="Submitted valid Task")
            
            # update task if needed.
            if task.completable == True:
                with reversion.create_revision():
                    task.done = True
                    task.save()
                
                task_log(request, task=task, message="Completed Task")
                                       
            # if we have a file saved and a language then add it to the attachments...
            if task.language and task.source and (task.image or task.file):
                from website.apps.core.models import Attachment
                if task.image:
                    a = Attachment.objects.create(
                        editor = request.user,
                        language = task.language,
                        source = task.source,
                        file = task.image
                    )
                if task.file:
                    a = Attachment.objects.create(
                        editor = request.user,
                        language = task.language,
                        source = task.source,
                        file = task.file
                    )
            
            return render_to_response('entry/done.html', {
                'task': task,
                'objects': completed,
            }, context_instance=RequestContext(request))
        else:
            task_log(request, task=task, message="Submitted incomplete")
            

@login_required()
def GenericView(request, task):
    """Generic data entry task"""
    template_name = "entry/formtemplates/generic.html"
    # process form
    if request.POST:
        formset = GenericFormset(request.POST)
        process_post_and_save(request, task, formset)
    else:
        # set up initial data
        initial = {}
        if task.language:
            initial['language'] = task.language
        if task.source:
            initial['source'] = task.source
        formset = GenericFormset(initial=[initial for i in range(task.records)])
    
    return render_to_response('entry/detail.html', {
        'task': task,
        'formset': formset,
        'template': template_name,
    }, context_instance=RequestContext(request))

