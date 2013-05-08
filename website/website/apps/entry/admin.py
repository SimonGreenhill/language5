from django.contrib import admin
from reversion.admin import VersionAdmin
from website.apps.entry.models import Task, TaskLog
from website.apps.core.admin import TrackedModelAdmin

class CheckpointListFilter(admin.SimpleListFilter):
    title = 'Has Checkpoint'
    
    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'has_checkpoint'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('yes', 'Has Checkpoint'),
            ('no', 'No Checkpoint'),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value() == 'yes':
            return queryset.filter(checkpoint__isnull=False).exclude(checkpoint__iexact='')
        if self.value() == 'no':
            return queryset.filter(checkpoint__isnull=True).filter(checkpoint__exact='')

class TaskAdmin(TrackedModelAdmin, VersionAdmin):
    date_hierarchy = 'added'
    list_display = ('name', 'source', 'language', 'records', 'view', 'added', 'completable', 'done')
    list_filter = ('editor', 'done', 'completable', CheckpointListFilter, 'source', 'language', 'view')
    ordering = ('name',)


class TaskLogAdmin(admin.ModelAdmin):
    date_hierarchy = 'time'
    list_display = ('person', 'time', 'page', 'message')
    list_filter = ('person', 'page',)
    ordering = ('time',)


admin.site.register(Task, TaskAdmin)
admin.site.register(TaskLog, TaskLogAdmin)


