from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from django import forms
from django.forms.formsets import formset_factory

from website.apps.lexicon.models import Lexicon


class GenericForm(forms.ModelForm):
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

GenericFormSet = formset_factory(GenericForm, extra=40)


@login_required()
def GenericView(request, task):
    """Generic Data Entry Task"""
    template_name = "entry/formtemplates/generic.html"
    
    # process form
    if request.method == 'POST':
        form = GenericForm(request.POST)
        if form.is_valid():
            # two stages here to set default fields
            obj = form.save(commit=False)
            obj.editor = request.user
            obj.save()
            # update task
            task.done = True
            task.save()
            
            return render_to_response('entry/done.html', {
                'task': task,
                'objects': [obj],
            }, context_instance=RequestContext(request))
    else:
        form = GenericForm()
    
    return render_to_response('entry/detail.html', {
        'task': task,
        'form': form,
        'template': template_name,
    }, context_instance=RequestContext(request))

