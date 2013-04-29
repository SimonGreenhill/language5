from django.contrib import admin
from reversion.admin import VersionAdmin
from website.apps.entry.models import Task, TaskLog
from website.apps.core.admin import TrackedModelAdmin

class TaskAdmin(TrackedModelAdmin, VersionAdmin):
    date_hierarchy = 'added'
    list_display = ('name', 'source', 'language', 'records', 'view', 'added', 'completable', 'done')
    list_filter = ('editor', 'source', 'language', 'view', 'done')
    ordering = ('name',)


class TaskLogAdmin(admin.ModelAdmin):
    date_hierarchy = 'time'
    list_display = ('person', 'time', 'page', 'message')
    list_filter = ('person', 'page',)
    ordering = ('time',)


admin.site.register(Task, TaskAdmin)
admin.site.register(TaskLog, TaskLogAdmin)


