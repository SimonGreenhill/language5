# This lists the available data-entry views

from generic import GenericView
from wordlist import WordlistView

available_views = [
    ('GenericView', GenericView.__doc__),
    ('WordlistView', WordlistView.__doc__),
]
