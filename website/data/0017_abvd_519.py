
import os
from tools import ABVDImporter

from django.contrib.auth.models import User
from website.apps.core.models import Source, Language
from website.apps.lexicon.models import Word, Lexicon

DATAFILE = "{}.json.gz".format(os.path.splitext(os.environ['IMPORTER_FILENAME'])[0])
importer = ABVDImporter(DATAFILE, editor=User.objects.get(pk=1)).install()
