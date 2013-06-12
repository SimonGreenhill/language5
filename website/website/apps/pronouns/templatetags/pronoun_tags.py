from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe
register = template.Library()

def form_fielderror_hint(field):
    if field.errors:
        errs = []
        for error in field.errors:
            errs.append(escape(error))
        
        return mark_safe("""
        <i class="tip icon-exclamation-sign" 
            data-toggle="tooltip" 
            data-placement="top" 
            data-container="td"
            title="%s">
        </i>
        """ % ",".join(errs))
    else:
        return mark_safe("")


register.filter('form_fielderror_hint', form_fielderror_hint)
