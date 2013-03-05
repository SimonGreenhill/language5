from django.db.models import Count
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from website.apps.entry.models import Task
from website.apps.forms import *

# ----------------------------------------------------------- #
#
# Specific tasks
#
# ----------------------------------------------------------- #

@login_required()
def generic(request, task_id):
    """Generic Data Entry Task"""
    template_name = "entry/formtemplates/generic.html"
    form = GenericForm(initial={'editor': request.user})
    return render_to_response('entry/detail.html', {
        'task': t,
        'form': form,
        'template': template_name,
    }, context_instance=RequestContext(request))
    



# This lists the available data-entry views
EntryViews = [
    ('generic', generic.__doc__),


]
