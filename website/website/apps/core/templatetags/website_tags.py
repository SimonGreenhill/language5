from django import template
from django.core.urlresolvers import resolve

register = template.Library()

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