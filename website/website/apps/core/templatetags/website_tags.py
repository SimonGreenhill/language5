from django import template
from django.urls import resolve
from website.apps.core.models import Language, Location
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
def link_glottolog(lang):
    """Links to the Glottolog"""
    if isinstance(lang, Language) and lang.glottocode:
        return "http://glottolog.org/resource/languoid/id/%s" % lang.glottocode
    else:
        return ""

@register.filter
def link_olac(lang):
    """Links to the OLAC project"""
    if isinstance(lang, Language) and lang.isocode:
        return "https://www.language-archives.org/language/%s" % lang.isocode
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
    return {'classif': [_.strip() for _ in classification.split(",")] if classification else []}

@register.filter
def classification_nodes(classification):
    """Splits a classification string into its nodes"""
    return [_.strip() for _ in classification.split(",") if _.strip()] if classification else []

@register.inclusion_tag('includes/map.html')
def show_map(location, language=None, radius=7):
    """Map centred on `location`, with other TNG languages within `radius` degrees"""
    near = Location.objects.filter(
        latitude__range=(location.latitude - radius, location.latitude + radius),
        longitude__range=(location.longitude - radius, location.longitude + radius),
    ).exclude(isocode=location.isocode)
    coords = {loc.isocode: (loc.latitude, loc.longitude) for loc in near}
    nearby = {}
    # one marker per isocode; prefer the language over its dialects
    for lang in Language.objects.filter(isocode__in=coords).order_by('-dialect', 'language'):
        lat, lng = coords[lang.isocode]
        nearby[lang.isocode] = {'name': lang.language, 'url': lang.get_absolute_url(), 'lat': lat, 'lng': lng}
    return {
        'latitude': location.latitude,
        'longitude': location.longitude,
        'name': language.language if language else '',
        'nearby': list(nearby.values()),
    }

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

