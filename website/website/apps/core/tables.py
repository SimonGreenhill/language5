from django.utils.safestring import mark_safe
import django_tables2 as tables
from django_tables2.utils import A  # alias for Accessor
from django.template.loader import render_to_string

from website.apps.core.models import Source, Language, Family
from website.apps.core.templatetags.website_tags import condense_classification

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
        #order_by = ('author', 'year',)
        order_by = 'author'
        sequence = ('author', 'year', 'reference', 'count')
        exclude = ('id', 'editor', 'added', 'slug', 'comment', 'bibtex')
    Meta.attrs['summary'] = 'Table of Sources'
    

class LanguageIndexTable(DataTable):
    """Language Listing"""
    isocode = tables.LinkColumn('language-detail', args=[A('slug')])
    language = tables.LinkColumn('language-detail', args=[A('slug')])
    classification = tables.Column()
    count = tables.LinkColumn('language-detail', args=[A('slug')])
    
    def render_language(self, record):
        col = tables.LinkColumn('language-detail', args=[record.slug])
        return col.render(value=record, record=record, bound_column=None)
    
    def render_classification(self, record):
        return mark_safe(render_to_string(
            'includes/condense_classification.html', condense_classification(record.classification)
        ))
        
    class Meta(DataTable.Meta):
        model = Language
        order_by = 'language' # default sorting
        sequence = ('isocode', 'language', 'classification', 'count')
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
    
