import django_tables2 as tables
from django_tables2.utils import A  # alias for Accessor

from website.apps.core.tables import DataTable

from website.apps.pronouns.models import Paradigm, Pronoun, Relationship


class ParadigmIndexTable(DataTable):
    """Paradigm Listing"""
    language = tables.LinkColumn('pronouns:detail', args=[A('id')])
    edit = tables.LinkColumn("pronouns:edit", args=[A('id')])
    
    class Meta(DataTable.Meta):
        model = Paradigm
        order_by = 'language' # default sorting
        sequence = ('id', 'language', 'source')
        exclude = ('editor', 'added', 'comment')
    Meta.attrs['summary'] = 'Table of Paradigms'


class PronounTable(DataTable):
    """Pronoun Listing"""
    class Meta(DataTable.Meta):
        model = Pronoun
        order_by = 'id' # default sorting
        sequence = ('id', 'person', 'number', 'alignment', 'gloss', 'comment')
        exclude = ('editor', 'added', 'paradigm')
    Meta.attrs['summary'] = 'Table of Pronouns'


class PronounRelationshipTable(DataTable):
    """Pronoun Listing"""
    class Meta(DataTable.Meta):
        model = Relationship
        order_by = 'id' # default sorting
        sequence = ('pronoun1', 'pronoun2', 'relationship', 'comment')
        exclude = ('id', 'editor', 'added', 'paradigm')
    Meta.attrs['summary'] = 'Table of Pronoun Paradigm Relationship'