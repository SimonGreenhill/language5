# This lists the available data-entry views

from generic import GenericView
from franklin1973 import FranklinView

available_views = [
    ('GenericView', GenericView.__doc__),
    ('FranklinView', FranklinView.__doc__),
]
