# This lists the available data-entry views

from generic import GenericView
from franklin1973 import FranklinView
from wordlist import WordlistView

available_views = [
    ('GenericView', GenericView.__doc__),
    ('WordlistView', WordlistView.__doc__),
    ('FranklinView', FranklinView.__doc__), # TODO - DEPRECATE ME SOON
]
