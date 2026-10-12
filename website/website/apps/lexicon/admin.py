from django.contrib import admin
from django.db import models
from django.forms import Textarea
from reversion.admin import VersionAdmin

from website.apps.lexicon.models import Word, WordSubset, Lexicon
from website.apps.lexicon.models import CognateSet, Cognate, CognateNote
from website.apps.lexicon.models import CorrespondenceSet, Correspondence
from website.apps.lexicon.models import Concepticon

from website.apps.core.admin import TrackedModelAdmin


# Inlines
class CognatesInline(admin.TabularInline):
    model = Cognate
    extra = 0
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':1}) },
    }
    fields = ('lexicon', 'source', 'comment', 'editor')
    raw_id_fields = ('lexicon', )
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'editor':
            kwargs['initial'] = request.user
            return db_field.formfield(**kwargs)
        return super().formfield_for_foreignkey(
            db_field, request, **kwargs
        )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('source', 'lexicon')


class CorrespondenceInline(admin.TabularInline):
    model = Correspondence
    extra = 1
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'editor':
            kwargs['initial'] = request.user
            return db_field.formfield(**kwargs)
        return super().formfield_for_foreignkey(
            db_field, request, **kwargs
        )


# Admin Classes
@admin.register(Word)
class WordAdmin(TrackedModelAdmin, VersionAdmin):
    date_hierarchy = 'added'
    list_display = ('id', 'word', 'concepticon_id', 'full', 'quality', 'comment')
    list_filter = ('editor', 'quality')
    ordering = ('word',)
    prepopulated_fields = {'slug': ('word', )}
    search_fields = ('word', 'full', 'comment')
    

@admin.register(WordSubset)
class WordSubsetAdmin(TrackedModelAdmin, VersionAdmin):
    date_hierarchy = 'added'
    list_display = ('id', 'subset', 'description')
    list_filter = ('editor',)
    ordering = ('subset',)
    search_fields = ('subset', 'description')
    filter_horizontal = ('words',)


@admin.register(Lexicon)
class LexiconAdmin(TrackedModelAdmin, VersionAdmin):
    date_hierarchy = 'added'
    list_display = ('id', 'language', 'source', 'word', 'entry', 'source_gloss', 'annotation', 'loan')
    list_filter = ('editor', 'language', 'word', 'source', 'loan')
    search_fields = ('entry', 'word__word', 'source_gloss', 'annotation')
    ordering = ('id',)
    

@admin.register(CognateSet)
class CognateSetAdmin(TrackedModelAdmin, VersionAdmin):
    date_hierarchy = 'added'
    list_display = ('id', 'protoform', 'gloss', 'source', 'quality')
    list_filter = ('editor', 'source', 'quality')
    ordering = ('id',)
    list_select_related = True
    inlines = [CognatesInline]
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('source')


@admin.register(CorrespondenceSet)
class CorrespondenceSetAdmin(TrackedModelAdmin, VersionAdmin):
    date_hierarchy = 'added'
    list_display = ('id', 'source', 'comment')
    list_filter = ('editor', 'source', 'language')
    ordering = ('id',)
    inlines = [CorrespondenceInline]
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('source')


@admin.register(Cognate)
class CognateAdmin(TrackedModelAdmin, VersionAdmin):
    list_display = ('cognateset', 'source', 'lexicon')
    raw_id_fields = ('lexicon', 'cognateset', )
    list_filter = ('editor', 'source',)
    ordering = ('id',)
    list_select_related = True
    search_fields = ('cognateset__protoform', 'cognateset__gloss', 'source__slug', 'lexicon__entry', 'comment')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('source', 'cognateset', 'lexicon')


@admin.register(CognateNote)
class CognateNoteAdmin(TrackedModelAdmin, VersionAdmin):
    list_display = ('word', 'cognateset', 'editor', 'note')
    list_filter = ('word', 'editor',)
    ordering = ('id',)
    list_select_related = True
    search_fields = ('word', 'cognateset', 'editor', 'note')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('word', 'cognateset')


@admin.register(Correspondence)
class CorrespondenceAdmin(TrackedModelAdmin, VersionAdmin):
    list_display = ('corrset', 'language', 'rule')
    list_filter = ('corrset', 'language',)
    ordering = ('id',)
    list_select_related = True
    search_fields = ('language', 'rule')


@admin.register(Concepticon)
class ConcepticonAdmin(TrackedModelAdmin, VersionAdmin):
    list_display = ('id', 'gloss', 'semanticfield', 'definition', 'ontologicalcategory')
    list_filter = ('semanticfield', 'ontologicalcategory',)
    ordering = ('id',)
    list_select_related = True
    search_fields = ('gloss', 'definition')


