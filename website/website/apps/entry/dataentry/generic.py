from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from django import forms
from django.forms.formsets import formset_factory

from website.apps.core.models import Language, Source
from website.apps.lexicon.models import Lexicon, Word

class GenericForm(forms.ModelForm):
    language = forms.ModelChoiceField(queryset=Language.objects.order_by('slug'))
    word = forms.ModelChoiceField(queryset=Word.objects.order_by('word'))
    source = forms.ModelChoiceField(queryset=Source.objects.order_by('slug'))
    
    class Meta:
        model = Lexicon
        exclude = ('editor', 'phon_entry', 'loan', 'loan_source')
        widgets = {
            # over-ride Textarea for annotation
            'annotation': forms.widgets.TextInput(
                    attrs={'class': 'input-medium'}),
            
            # and set input-small
            'entry': forms.widgets.TextInput(attrs={'class': 'input-medium'}),
            'language': forms.widgets.Select(attrs={'class': 'input-medium'}),
            'source': forms.widgets.Select(attrs={'class': 'input-medium'}),
            'word': forms.widgets.Select(attrs={'class': 'input-medium'}),
        }
    # make sure to set editor, added, and loan if loan_source is specified

GenericFormSet = formset_factory(GenericForm, extra=0)


@login_required()
def GenericView(request, task):
    """Generic Data Entry Task"""
    template_name = "entry/formtemplates/generic.html"
    # process form
    if request.POST:
        formset = GenericFormSet(request.POST)
        if 'refresh' in request.POST:
            pass # Fall through
        elif 'submit' in request.POST:
            if formset.is_valid():
                completed = []
                for form in formset:
                    if form.is_valid() and len(form.changed_data):
                        # if form is valid and some fields have changed
                        # two stages here to set default fields
                        obj = form.save(commit=False)
                        obj.editor = request.user
                        obj.save()
                        completed.append(obj)
                    
                # update task if needed.
                if task.completable == True:
                    task.done = True
                    task.save()
            
                return render_to_response('entry/done.html', {
                    'task': task,
                    'objects': completed,
                }, context_instance=RequestContext(request))
    else:
        # set up initial data
        initial = {}
        if task.language:
            initial['language'] = task.language
        if task.source:
            initial['source'] = task.source
            
        formset = GenericFormSet(initial=[initial for i in range(task.records)])
    
    return render_to_response('entry/detail.html', {
        'task': task,
        'formset': formset,
        'template': template_name,
    }, context_instance=RequestContext(request))

