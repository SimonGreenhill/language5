from django import template
from django.core.urlresolvers import resolve

from ifinstalled import do_ifinstalled

register = template.Library()

def link_ethnologue(language):
    """Links to the Ethnologue"""
    if language.isocode:
        return "http://www.ethnologue.com/language/%s" % language.isocode
    else:
        return ""


def link_olac(language):
    """Links to the OLAC project"""
    if language.isocode:
        return "http://search.language-archives.org/search.html?q=%s" % language.isocode
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
register.filter('link_olac', link_olac)
register.filter('link_ethnologue', link_ethnologue)
register.tag('ifinstalled', do_ifinstalled)

