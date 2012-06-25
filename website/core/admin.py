from django.contrib import admin
from django import forms
from reversion.admin import VersionAdmin
from core.models import Language, AlternateNames, Family, Links, Locations

class LanguageAdmin(VersionAdmin):
    ##form = LanguageAdminForm
    list_display = ('language', 'isocode', 'added')
    inlines = []
    list_filter = ['added',] # ADD FAMILY
    date_hierarchy = 'added'
    search_fields = ['language', 'isocode']
    prepopulated_fields = {'slug': ('language', )}
    ordering = ['language']

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
