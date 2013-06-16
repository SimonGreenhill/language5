from django.contrib import admin
from reversion.admin import VersionAdmin
from website.apps.core.models import Language, AlternateName, Family
from website.apps.core.models import Link, Location, Source, Note

class TrackedModelAdmin(admin.ModelAdmin):
    """Mixin to automatically set editor field"""
    def add_view(self, request, form_url="", extra_context=None):
        data = request.GET.copy()
        data['editor'] = request.user.id
        request.GET = data
        return super(TrackedModelAdmin, self).add_view(request, form_url="", extra_context=extra_context)

# Inlines
class AltNameInline(admin.TabularInline):
    model = AlternateName
    extra = 0
    prepopulated_fields = {'slug': ('name', )}
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'editor':
            kwargs['initial'] = request.user
            return db_field.formfield(**kwargs)
        return super(AltNameInline, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )


# Admin
class LanguageAdmin(TrackedModelAdmin, VersionAdmin):
    date_hierarchy = 'added'
    list_display = ('language', 'dialect', 'isocode', 'added')
    list_filter = ('editor', 'family')
    ordering = ('language', 'dialect',)
    prepopulated_fields = {'slug': ('language', 'dialect',)}
    search_fields = ('language', 'dialect', 'isocode', 'alternatename__name')
    filter_horizontal = ('family', )
    inlines = [AltNameInline,]
    

class SourceAdmin(TrackedModelAdmin, VersionAdmin):
    date_hierarchy = 'added'
    list_filter = ('editor', 'author', 'year')
    ordering = ('author', 'year')
    prepopulated_fields = {'slug': ('author', 'year')}
    search_fields = ('author', 'year')


class NoteAdmin(TrackedModelAdmin, VersionAdmin):
    date_hierarchy = 'added'
    list_filter = ('editor', 'language', 'source')
    ordering = ('id',)
    search_fields = ('language', 'source', 'note')


class FamilyAdmin(TrackedModelAdmin, VersionAdmin):
    date_hierarchy = 'added'
    list_filter = ('editor',)
    ordering = ('family',)
    prepopulated_fields = {'slug': ('family', )}
    search_fields = ('family', )


class AlternateNameAdmin(TrackedModelAdmin, VersionAdmin):
    date_hierarchy = 'added'
    list_filter = ('editor', 'language')
    ordering = ('name',)
    search_fields = ('language', 'name')
    prepopulated_fields = {'slug': ('name', )}
    list_select_related = True


class LinkAdmin(TrackedModelAdmin, VersionAdmin):
    date_hierarchy = 'added'
    list_display = ('language', 'link', 'description')
    list_filter = ('editor', 'language', 'link')
    search_fields = ('language', 'link', 'description')


class LocationAdmin(TrackedModelAdmin, VersionAdmin):
    date_hierarchy = 'added'
    list_display = ('language', 'latitude', 'longitude')
    list_filter = ('editor', 'language', )


admin.site.register(Language, LanguageAdmin)
admin.site.register(Family, FamilyAdmin)
admin.site.register(AlternateName, AlternateNameAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(Note, NoteAdmin)
