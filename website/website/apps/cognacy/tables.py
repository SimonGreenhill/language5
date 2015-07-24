from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string

import django_tables2 as tables
from django_tables2.utils import A  # alias for Accessor

from website.apps.core.tables import DataTable

from website.apps.lexicon.models import Lexicon, CognateSet, Cognate
from website.apps.cognacy.templatetags.cognacy_tags import cognate_button
from website.apps.core.templatetags.website_tags import condense_classification


class CognateSetDetailTable(DataTable):
    """Cognate set detail table"""
    id = tables.Column()
    language = tables.LinkColumn('language-detail', args=[A('language.slug')])
    classification = tables.Column()
    word = tables.LinkColumn('word-detail', args=[A('word.slug')])
    source = tables.LinkColumn('source-detail', args=[A('source.slug')])
    entry = tables.Column()
    annotation = tables.Column()
    loan = tables.BooleanColumn(null=False, yesno=('x', ''))
    
    def render_language(self, record):
        col = tables.LinkColumn('language-detail', args=[record.language.slug])
        return col.render(value=unicode(record.language), record=unicode(record.language), bound_column=None)
    
    def render_classification(self, record):
        return mark_safe(render_to_string(
            'includes/condense_classification.html', 
            condense_classification(record.language.classification)
        ))
    
    class Meta(DataTable.Meta):
        model = Lexicon
        order_by = 'classification' # default sorting
        sequence = ('id', 'language', 'classification', 'word', 'entry', 'annotation', 'loan', 'source')
        exclude = ('editor', 'added', 'slug', 'phon_entry', 'loan_source', 'source_gloss', )
    Meta.attrs['summary'] = 'Table of Cognates'


class CognateSetIndexTable(DataTable):
    """Table of cognate sets"""
    id = tables.LinkColumn('cognacy:detail', args=[A('id')])
    protoform = tables.LinkColumn('cognacy:detail', args=[A('id')])
    gloss = tables.LinkColumn('cognacy:detail', args=[A('id')])
    count = tables.Column()
    source = tables.LinkColumn('source-detail', args=[A('source.slug')])
    
    class Meta(DataTable.Meta):
        model = CognateSet
        order_by = 'id' # default sorting
        sequence = ('id', 'protoform', 'gloss', 'count', 'source', )
        exclude = ('editor', 'added', 'comment', 'lexicon', 'quality')
    Meta.attrs['summary'] = 'Table of Cognate Sets'


class CognacyTable(DataTable):
    """Do Cognacy Table"""
    id = tables.LinkColumn('lexicon-edit', args=[A('id')])
    language = tables.LinkColumn('language-detail', args=[A('language.slug')])
    source = tables.LinkColumn('source-detail', args=[A('source.slug')])
    classification = tables.Column()
    entry = tables.Column()
    annotation = tables.Column()
    loan = tables.BooleanColumn(null=False, yesno=('x', ''))
    cognacy = tables.Column()
    edit = tables.Column()
    
    def render_language(self, record):
        col = tables.LinkColumn('language-detail', args=[record.language.slug])
        return col.render(value=unicode(record.language), record=unicode(record.language), bound_column=None)
    
    def render_cognacy(self, record):
        return mark_safe(
            " ".join([
                render_to_string('cognacy/includes/button.html', cognate_button(c)) for c in sorted(record.cognacy)
            ])
        )
    
    def render_edit(self, record):
        return mark_safe(
            '<input type="text" class="input-mini" id="c-%d" name="c-%d" value="" />' % (record.id, record.id)
        )
    
    def render_classification(self, record):
        return mark_safe(render_to_string(
            'includes/condense_classification.html', condense_classification(record.classification)
        ))
        
    class Meta(DataTable.Meta):
        model = Lexicon
        order_by = 'classification' # default sorting
        sequence = ('id', 'language', 'source', 'classification', 'entry', 'annotation', 'loan', 'cognacy', 'edit')
        exclude = ('editor', 'added', 'slug', 'phon_entry', 'loan_source', 'word', 'source_gloss')
    Meta.attrs['summary'] = 'Table of Lexicon'

