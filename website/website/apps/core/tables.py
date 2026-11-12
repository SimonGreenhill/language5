from django.utils.html import format_html, format_html_join
import django_tables2 as tables
from django_tables2.utils import A  # alias for Accessor

from website.apps.core.models import Source, Language, Family
from website.apps.core.templatetags.website_tags import classification_nodes

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
        default = ''
        attrs = {
            'class': "table table-bordered table-sm",
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
        order_by = 'author'
        sequence = ('author', 'year', 'reference', 'count')
        exclude = ('id', 'editor', 'added', 'slug', 'comment', 'bibtex')
    Meta.attrs['summary'] = 'Table of Sources'
    

class LanguageIndexTable(DataTable):
    """Language Listing"""
    isocode = tables.LinkColumn('language-detail', args=[A('slug')])
    glottocode = tables.LinkColumn('language-detail', args=[A('slug')])
    language = tables.LinkColumn('language-detail', args=[A('slug')])
    classification = tables.Column()
    count = tables.LinkColumn('language-detail', args=[A('slug')])
    
    def render_language(self, record):
        return str(record)
    
    def render_classification(self, record):
        """Top node (linked to the family page) › … › lowest subgroup; full path on hover"""
        nodes = classification_nodes(record.classification)
        if not nodes:
            return ''
        family = next(iter(record.family.all()), None)
        top = format_html('<a href="{}">{}</a>', family.get_absolute_url(), nodes[0]) if family else nodes[0]
        shown = [top] + (['…'] if len(nodes) > 2 else []) + ([nodes[-1]] if len(nodes) > 1 else [])
        return format_html('<span title="{}">{}</span>', ', '.join(nodes),
                           format_html_join(' › ', '{}', ((n,) for n in shown)))

    class Meta(DataTable.Meta):
        model = Language
        order_by = 'language' # default sorting
        sequence = ('isocode', 'glottocode', 'language', 'classification', 'count')
        exclude = ('id', 'editor', 'added', 'slug', 'information', 'dialect')
    Meta.attrs['summary'] = 'Table of Languages'


class FamilyIndexTable(DataTable):
    """Family Listing"""
    family = tables.LinkColumn('family-detail', args=[A('slug')])
    glottocode = tables.Column()
    count = tables.LinkColumn('family-detail', args=[A('slug')])

    def render_glottocode(self, value):
        return format_html('<a href="https://glottolog.org/resource/languoid/id/{0}">{0}</a>', value)

    class Meta(DataTable.Meta):
        model = Family
        order_by = 'family' # default sorting
        sequence = ('family', 'glottocode', 'count')
        exclude = ('id', 'editor', 'added', 'slug', 'glottolog_tree')
    Meta.attrs['summary'] = 'Table of Language Families'
    
