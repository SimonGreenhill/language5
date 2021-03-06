from django import template
from django.core.urlresolvers import resolve
from django.utils.safestring import mark_safe
from website.apps.core.models import Language
from website.apps.core.templatetags.ifinstalled import do_ifinstalled

register = template.Library()

@register.filter
def link_ethnologue(lang):
    """Links to the Ethnologue"""
    if isinstance(lang, Language) and lang.isocode:
        return "http://www.ethnologue.com/language/%s" % lang.isocode
    else:
        return ""

@register.filter
def link_olac(lang):
    """Links to the OLAC project"""
    if isinstance(lang, Language) and lang.isocode:
        return "http://search.language-archives.org/search.html?q=%s" % lang.isocode
    else:
        return ""

@register.filter
def link_multitree(lang):
    """Links to MultiTree"""
    if isinstance(lang, Language) and lang.isocode:
        return "http://multitree.org/codes/%s" % lang.isocode
    else:
        return ""

@register.filter
def link_glottolog(lang):
    """Links to Glottolog"""
    if isinstance(lang, Language) and lang.isocode:
        return "http://glottolog.org/resource/languoid/iso/%s" % lang.isocode
    else:
        return ""

@register.filter
def link_wikipedia(lang):
    """Links to Wikipedia"""
    if isinstance(lang, Language) and lang.isocode:
        return "https://en.wikipedia.org/wiki/ISO_639:%s" % lang.isocode
    else:
        return ""

@register.inclusion_tag('includes/condense_classification.html')
def condense_classification(classification):
    """Returns a condensed classification string"""
    return { 'classif': [_.strip() for _ in classification.split(",")] }

@register.inclusion_tag('includes/map.html')
def show_map(location):
    return {'latitude': location.latitude, 'longitude': location.longitude}

def active(context, view):
    try:
        resolved = resolve(context['request'].path_info)
    except KeyError:
        return ''

    if resolved.view_name == view:
        return ' class="active" '
    else:
        return ''

register.simple_tag(takes_context=True)(active)
register.tag('ifinstalled', do_ifinstalled)

