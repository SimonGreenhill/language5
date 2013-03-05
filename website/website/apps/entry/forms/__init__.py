# Add forms here to ensure they load!

from website.apps.entry.forms.SimpleForm import SimpleForm

entry_forms = [
    (SimpleForm.__name__, SimpleForm.description),
]


