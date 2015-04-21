from hashlib import md5

from django import template

register = template.Library()

def get_color(n):
    hash = md5(str(n)).hexdigest()
    n = float(n)
    if n % 1 == 0 or n % 5 == 0:
        hash = hash[0:6]
    elif n % 2 == 0 or n % 6 == 0:
        hash = hash[6:12]
    elif n % 3 == 0 or n % 7 == 0:
        hash = hash[12:18]
    elif n % 4 == 0 or n % 8 == 0:
        hash = hash[18:24]
    else:
        hash = hash[24:30]
    return '#%s' % hash

@register.inclusion_tag('cognacy/includes/button.html')
def cognate_button(cog_id):
    return {'id': cog_id, 'color': get_color(cog_id)}

