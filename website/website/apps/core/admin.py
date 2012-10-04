from django.contrib import admin
from reversion.admin import VersionAdmin
from website.apps.core.models import Language, AlternateNames, Family
from website.apps.core.models import Links, Locations, Source, Note

class LanguageAdmin(VersionAdmin):
    ##form = LanguageAdminForm
    list_display = ('language', 'isocode', 'added')
    inlines = []
    list_filter = ['added',] # ADD FAMILY
    date_hierarchy = 'added'
    search_fields = ['language', 'isocode']
    prepopulated_fields = {'slug': ('language', )}
    ordering = ['language']

class SourceAdmin(VersionAdmin):
    prepopulated_fields = {'slug': ('author', 'year')}
    date_hierarchy = 'year'
    list_filter = ['author', 'year']

class NoteAdmin(VersionAdmin):
    list_filter = ['language', 'source']

class FamilyAdmin(VersionAdmin):
    pass

class AlternateNamesAdmin(VersionAdmin):
    pass

class LinksAdmin(VersionAdmin):
    pass

class LocationsAdmin(VersionAdmin):
    pass


admin.site.register(Language, LanguageAdmin)
admin.site.register(Family, FamilyAdmin)
admin.site.register(AlternateNames, AlternateNamesAdmin)
admin.site.register(Links, LinksAdmin)
admin.site.register(Locations, LocationsAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(Note, NoteAdmin)
