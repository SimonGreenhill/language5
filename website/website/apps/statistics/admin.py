from django.contrib import admin
from website.apps.statistic.models import StatisticalValue

class StatisticalValueAdmin(TrackedModelAdmin, VersionAdmin):
    date_hierarchy = 'date'
    list_display = ('label', 'model', 'method')
    list_filter = ('label',)
    ordering = ('date',)

admin.site.register(StatisticalValue, StatisticalValueAdmin)
