from django.contrib import admin
from reversion.admin import VersionAdmin
from website.apps.statistics.models import StatisticalValue

class StatisticalValueAdmin(TrackedModelAdmin, VersionAdmin):
    date_hierarchy = 'date'
    list_display = ('label', 'model', 'value')
    list_filter = ('label', 'model',)
    ordering = ('date',)

admin.site.register(StatisticalValue, StatisticalValueAdmin)
