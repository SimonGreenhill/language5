from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from django import forms
from django.forms.formsets import formset_factory

from website.apps.core.models import Language, Source
from website.apps.lexicon.models import Lexicon, Word

from generic import GenericFormSet

@login_required()
def FranklinView(request, task):
    """Data Entry Task for Franklin 1973"""
    template_name = "entry/formtemplates/franklin.html"
    
    # Note - put this here, it'll only get instantiated once this view is called.
    WORDS = {
        1: Word.objects.get(slug="man"),
        2: Word.objects.get(slug="woman"),
        3: Word.objects.get(slug="i"),
        4: Word.objects.get(slug="thou"),
        5: Word.objects.get(slug="we-incl"), # ADD INCL/EXCL
        6: Word.objects.get(slug="all"),
        7: Word.objects.get(slug="head"),
        8: Word.objects.get(slug="hair"),
        9: Word.objects.get(slug="eye"),
        10: Word.objects.get(slug="nose"),
        
        11: Word.objects.get(slug="ear"),
        12: Word.objects.get(slug="tooth"),
        13: Word.objects.get(slug="tongue"),
        14: Word.objects.get(slug="neck"),
        15: Word.objects.get(slug="mouth"),
        16: Word.objects.get(slug="arm"), # ADD ARM
        17: Word.objects.get(slug="breast"),
        18: Word.objects.get(slug="belly"),
        19: Word.objects.get(slug="leg"),
        20: Word.objects.get(slug="knee"),
        
        21: Word.objects.get(slug="skin"),
        22: Word.objects.get(slug="blood"),
        23: Word.objects.get(slug="fat"),
        24: Word.objects.get(slug="bone"),
        25: Word.objects.get(slug="heart"),
        26: Word.objects.get(slug="liver"),
        27: Word.objects.get(slug="sun"),
        28: Word.objects.get(slug="moon"),
        29: Word.objects.get(slug="star"),
        30: Word.objects.get(slug="cloud"),
        
        31: Word.objects.get(slug="rain"), 
        32: Word.objects.get(slug="night"),
        33: Word.objects.get(slug="water"),
        34: Word.objects.get(slug="ground"),
        35: Word.objects.get(slug="stone"),
        36: Word.objects.get(slug="sand"),
        37: Word.objects.get(slug="mountain"),
        38: Word.objects.get(slug="fire"),
        39: Word.objects.get(slug="smoke"),
        40: Word.objects.get(slug="ashes"),
        
        41: Word.objects.get(slug="road"), # change to road/path
        42: Word.objects.get(slug="tree"),
        43: Word.objects.get(slug="root"),
        44: Word.objects.get(slug="bark"),
        45: Word.objects.get(slug="dog"),
        46: Word.objects.get(slug="tail"),
        47: Word.objects.get(slug="bird"),
        48: Word.objects.get(slug="feather"),
        49: Word.objects.get(slug="egg"),
        50: Word.objects.get(slug="fish"),
        
        51: Word.objects.get(slug="big"),
        52: Word.objects.get(slug="small"),
        53: Word.objects.get(slug="good"),
        54: Word.objects.get(slug="long"),
        55: Word.objects.get(slug="red"),
        56: Word.objects.get(slug="white"),
        57: Word.objects.get(slug="black"),
        58: Word.objects.get(slug="yellow"),
        59: Word.objects.get(slug="green"),
        60: Word.objects.get(slug="warm"), # change to warm/hot
        
        61: Word.objects.get(slug="cold"),
        62: Word.objects.get(slug="full"),
        63: Word.objects.get(slug="new"),
        64: Word.objects.get(slug="to-eat"),
        65: Word.objects.get(slug="to-drink"),
        66: Word.objects.get(slug="to-stand"),
        67: Word.objects.get(slug="to-sit"),
        68: Word.objects.get(slug="to-speak"), # change to say, speak
        69: Word.objects.get(slug="to-walk"),
        70: Word.objects.get(slug="to-give"),
        
        71: Word.objects.get(slug="to-sleep"),
        72: Word.objects.get(slug="to-lie"), # ChANGE to lie - to lie down
        73: Word.objects.get(slug="to-see"),
        74: Word.objects.get(slug="to-hear"),
        75: Word.objects.get(slug="to-swim"),
        76: Word.objects.get(slug="to-come"),
        77: Word.objects.get(slug="to-fly"),
        78: Word.objects.get(slug="to-bite"),
        79: Word.objects.get(slug="name"),
        80: Word.objects.get(slug="dry"),
        
        81: Word.objects.get(slug="who"),
        82: Word.objects.get(slug="what"),
        83: Word.objects.get(slug="to-burn"),
        84: Word.objects.get(slug="louse"),
        85: Word.objects.get(slug="many"),
        86: Word.objects.get(slug="this"),
        87: Word.objects.get(slug="that"),
        88: Word.objects.get(slug="one"),
        89: Word.objects.get(slug="two"),
        90: Word.objects.get(slug="to-know"),
        
        91: Word.objects.get(slug="to-kill"),
        92: Word.objects.get(slug="not"),
        93: Word.objects.get(slug="leaf"),
        94: Word.objects.get(slug="meat"),
        95: Word.objects.get(slug="horn"),
        96: Word.objects.get(slug="claw"),
        97: Word.objects.get(slug="person"),
        98: Word.objects.get(slug="seed"),
        99: Word.objects.get(slug="round"),
        100: Word.objects.get(slug="to-die")
    }
    
    # process form
    if request.method == 'POST':
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
        initial = []
        for i in range(1, 101):
            initial.append({
                'language': task.language,
                'source': task.source,
                'word': WORDS[i],
            })
        formset = GenericFormSet(initial=initial)
    
    return render_to_response('entry/detail.html', {
        'task': task,
        'formset': formset,
        'template': template_name,
    }, context_instance=RequestContext(request))

