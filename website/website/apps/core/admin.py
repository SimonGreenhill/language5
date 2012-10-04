from django.contrib import admin
from reversion.admin import VersionAdmin
from website.apps.core.models import Language, AlternateName, Family
from website.apps.core.models import Link, Location, Source, Note

class LanguageAdmin(VersionAdmin):
    ##form = LanguageAdminForm
    list_display = ('language', 'isocode', 'added')
    inlines = []
    list_filter = ['added',] # ADD FAMILY?
    date_hierarchy = 'added'
    search_fields = ['language', 'isocode']
    prepopulated_fields = {'slug': ('language', )}
    ordering = ['language']

class SourceAdmin(VersionAdmin):
    prepopulated_fields = {'slug': ('author', 'year')}
    list_filter = ['author', 'year']

class NoteAdmin(VersionAdmin):
    list_filter = ['language', 'source']

class FamilyAdmin(VersionAdmin):
    pass

class AlternateNameAdmin(VersionAdmin):
    pass

class LinkAdmin(VersionAdmin):
    pass

class LocationAdmin(VersionAdmin):
    pass


admin.site.register(Language, LanguageAdmin)
admin.site.register(Family, FamilyAdmin)
admin.site.register(AlternateName, AlternateNameAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(Note, NoteAdmin)
