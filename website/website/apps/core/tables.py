import django_tables2 as tables
from django_tables2.utils import A  # alias for Accessor

from website.apps.core.models import Source, Language, Family

# Note, due to the current version of django_tables2 not merging in Meta classes
# https://github.com/bradleyayers/django-tables2/issues/85
# The work around is to inherit class Meta in the subclasses e.g.
# class Child(DataTable):
#     class Meta(DataTable.Meta):
#         pass
#
# another annoyance is that you can't override anything in Meta - it'll cause a 
# NameError to be raised. The work around is this:
#
# class Child(DataTable):
#     class Meta(DataTable.Meta):
#         pass
#     Meta.var = X
#
# Ugly, but it works.

class DataTable(tables.Table):
    """Parent class for Datatables"""
    class Meta:
        orderable = True
        default = u''
        attrs = {
            'class': "table table-bordered table-condensed",
            'summary': '',
        }
    

class SourceIndexTable(DataTable):
    """Source Listing"""
    author = tables.LinkColumn('source-detail', args=[A('slug')])
    year = tables.LinkColumn('source-detail', args=[A('slug')])
    reference = tables.LinkColumn('source-detail', args=[A('slug')])
    count = tables.LinkColumn('source-detail', args=[A('slug')])
    
    class Meta(DataTable.Meta):
        model = Source
        order_by = 'author' # default sorting
        sequence = ('author', 'year', 'reference', 'count')
        exclude = ('id', 'editor', 'added', 'slug', 'comment', 'bibtex')
    Meta.attrs['summary'] = 'Table of Sources'
    

class LanguageIndexTable(DataTable):
    """Language Listing"""
    isocode = tables.LinkColumn('language-detail', args=[A('slug')])
    language = tables.LinkColumn('language-detail', args=[A('slug')])
    count = tables.LinkColumn('language-detail', args=[A('slug')])
    
    def render_language(self, record):
        return unicode(record)
        
    class Meta(DataTable.Meta):
        model = Language
        order_by = 'language' # default sorting
        sequence = ('isocode', 'language', 'count', 'classification')
        exclude = ('id', 'editor', 'added', 'slug', 'information', 'dialect')
    Meta.attrs['summary'] = 'Table of Languages'


class FamilyIndexTable(DataTable):
    """Family Listing"""
    family = tables.LinkColumn('family-detail', args=[A('slug')])
    count = tables.LinkColumn('family-detail', args=[A('slug')])
    
    class Meta(DataTable.Meta):
        model = Family
        order_by = 'family' # default sorting
        sequence = ('family', 'count')
        exclude = ('id', 'editor', 'added', 'slug')
    Meta.attrs['summary'] = 'Table of Language Families'
    
