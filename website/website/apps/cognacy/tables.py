from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string

import django_tables2 as tables
from django_tables2.utils import A  # alias for Accessor

from website.apps.core.tables import DataTable

from website.apps.core.models import Source
from website.apps.lexicon.models import Lexicon, CognateSet, Cognate
from website.apps.cognacy.templatetags.cognacy_tags import cognate_button
from website.apps.core.templatetags.website_tags import condense_classification


class CognateSourceIndexTable(DataTable):
    """Table of cognate sets by source"""
    reference = tables.LinkColumn('cognacy:cognatesource_detail', args=[A('slug')])
    count = tables.Column()
    
    class Meta(DataTable.Meta):
        model = Source
        order_by = 'author' # default sorting
        sequence = ('reference', 'count',)
        exclude = (
            'id', 'editor', 'added', 'comment', 'quality', 'slug', 'bibtex', 'author', 'year'
        )
    Meta.attrs['summary'] = 'Table of Sources with Cognates'


class CognateSourceDetailTable(DataTable):
    """Table of cognate sets by source"""
    cognateset = tables.LinkColumn('cognacy:detail', args=[A('cognateset_id')])
    language = tables.LinkColumn('language-detail', args=[A('language.slug')])
    word = tables.LinkColumn('word-detail', args=[A('word.slug')])
    lexicon = tables.Column()
    
    def render_lexicon(self, record):
        col = tables.Column()
        return col.render(value=record.lexicon.entry)
    
    def render_cognateset(self, record):
        return mark_safe(
            render_to_string('cognacy/includes/button.html', cognate_button(record.cognateset_id))
        )
    
    class Meta(DataTable.Meta):
        model = Cognate
        order_by = 'cognateset_id' # default sorting
        sequence = ('cognateset', 'language', 'word', 'lexicon', )
        exclude = ('id', 'editor', 'added', 'comment', 'quality', 'flag', 'source')
    Meta.attrs['summary'] = 'Table of Cognate Sets by Source'


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
        return col.render(value=record.language, record=record.language, bound_column=None)
    
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
        return col.render(value=record.language, record=record.language, bound_column=None)
    
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

