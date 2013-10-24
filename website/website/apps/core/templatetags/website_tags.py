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
def link_llmap(lang):
    """Links to LLMap"""
    if isinstance(lang, Language) and lang.isocode:
        return "http://llmap.org/languages/%s.html" % lang.isocode
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
def language_map(lang):
    """Embeds a link to LLMap"""
    WIDTH = 400
    HEIGHT = 300
    
    if isinstance(lang, Language) and lang.isocode:
        return mark_safe("""
        <img src="http://llmap.org/language/%s.png?width=%d&height=%d" alt="Map of %s: courtesy of LL-MAP" />
        """ % (lang.isocode, WIDTH, HEIGHT, unicode(lang))
        ).strip()
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

