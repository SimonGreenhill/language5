from django.contrib import admin
from django.db import models
from django.forms import Textarea
from reversion.admin import VersionAdmin

from website.apps.lexicon.models import Word, WordSubset, Lexicon
from website.apps.lexicon.models import CognateSet, Cognate
from website.apps.lexicon.models import CorrespondenceSet, Correspondence

from website.apps.core.admin import TrackedModelAdmin


# Inlines
class CognatesInline(admin.TabularInline):
    model = Cognate
    extra = 1
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':1}) },
    }
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'editor':
            kwargs['initial'] = request.user
            return db_field.formfield(**kwargs)
        return super(CognatesInline, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )


class CorrespondenceInline(admin.TabularInline):
    model = Correspondence
    extra = 1
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'editor':
            kwargs['initial'] = request.user
            return db_field.formfield(**kwargs)
        return super(CorrespondenceInline, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )


# Admin Classes
class WordAdmin(TrackedModelAdmin, VersionAdmin):
    date_hierarchy = 'added'
    list_display = ('id', 'word', 'slug', 'full', 'quality', 'comment')
    list_filter = ('editor', 'quality')
    ordering = ('word',)
    prepopulated_fields = {'slug': ('word', )}
    search_fields = ('word', 'full', 'comment')
    

class WordSubsetAdmin(TrackedModelAdmin, VersionAdmin):
    date_hierarchy = 'added'
    list_display = ('id', 'subset', 'description')
    list_filter = ('editor',)
    ordering = ('subset',)
    search_fields = ('subset', 'description')
    filter_horizontal = ('words',)


class LexiconAdmin(TrackedModelAdmin, VersionAdmin):
    date_hierarchy = 'added'
    list_display = ('id', 'language', 'source', 'word', 'entry', 'annotation', 'loan')
    list_filter = ('editor', 'language', 'word', 'source', 'loan')
    search_fields = ('entry', 'word__word', 'annotation')
    ordering = ('id',)
    

class CognateSetAdmin(TrackedModelAdmin, VersionAdmin):
    date_hierarchy = 'added'
    list_display = ('id', 'protoform', 'gloss', 'source', 'comment', 'quality')
    list_filter = ('editor', 'source', 'quality')
    ordering = ('id',)
    list_select_related = True
    inlines = [CognatesInline]
    
    def queryset(self, request):
        return super(CognateSetAdmin, self).queryset(request).select_related('source')


class CorrespondenceSetAdmin(TrackedModelAdmin, VersionAdmin):
    date_hierarchy = 'added'
    list_display = ('id', 'source', 'comment')
    list_filter = ('editor', 'source', 'language')
    ordering = ('id',)
    inlines = [CorrespondenceInline]
    
    def queryset(self, request):
        return super(CorrespondenceSetAdmin, self).queryset(request).select_related('source', 'language')


class CognateAdmin(TrackedModelAdmin, VersionAdmin):
    list_display = ('cognateset', 'lexicon', 'source', 'comment', 'flag')
    list_filter = ('editor', 'cognateset', 'source', 'lexicon')
    ordering = ('id',)
    list_select_related = True
    
    def queryset(self, request):
        return super(CognateAdmin, self).queryset(request).select_related('lexicon', 'source', 'cognateset')


class CorrespondenceAdmin(TrackedModelAdmin, VersionAdmin):
    pass



admin.site.register(Word, WordAdmin)
admin.site.register(WordSubset, WordSubsetAdmin)
admin.site.register(Lexicon, LexiconAdmin)
admin.site.register(CognateSet, CognateSetAdmin)
admin.site.register(CorrespondenceSet, CorrespondenceSetAdmin)
admin.site.register(Cognate, CognateAdmin)
admin.site.register(Correspondence, CorrespondenceAdmin)
