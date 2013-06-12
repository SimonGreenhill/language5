from django import template
from django.core.urlresolvers import resolve
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from ifinstalled import do_ifinstalled

register = template.Library()

@register.filter
def link_ethnologue(language):
    """Links to the Ethnologue"""
    if language.isocode:
        return "http://www.ethnologue.com/language/%s" % language.isocode
    else:
        return ""

@register.filter
def link_olac(language):
    """Links to the OLAC project"""
    if language.isocode:
        return "http://search.language-archives.org/search.html?q=%s" % language.isocode
    else:
        return ""

@register.filter
def link_llmap(language):
    if language.isocode:
        return "http://llmap.org/languages/%s.html" % language.isocode
    else:
        return ""

@register.filter
def link_multitree(language):
    if language.isocode:
        return "http://multitree.org/codes/%s" % language.isocode
    else:
        return ""

@register.filter
def language_map(language):
    """Embeds a link to LLMap"""
    WIDTH = 400
    HEIGHT = 300
    
    if language.isocode:
        return mark_safe("""
        <img src="http://llmap.org/language/%s.png?width=%d&height=%d" alt="Map of %s: courtesy of LL-MAP" />
        """ % (language.isocode, WIDTH, HEIGHT, unicode(language))
        )
    else:
        return ""


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

