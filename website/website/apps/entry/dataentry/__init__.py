# This lists the available data-entry views

from generic import GenericView
from franklin1973 import FranklinView
from shaw1986 import ShawView

available_views = [
    ('GenericView', GenericView.__doc__),
    ('FranklinView', FranklinView.__doc__),
    ('ShawView', ShawView.__doc__),
]
