from django.contrib import admin
from reversion.admin import VersionAdmin
from website.apps.entry.models import Task
from website.apps.core.admin import TrackedModelAdmin


class TaskAdmin(TrackedModelAdmin, VersionAdmin):
    date_hierarchy = 'added'
    list_display = ('name', 'source', 'language', 'records', 'view', 'added', 'completable', 'done')
    list_filter = ('editor', 'source', 'language', 'view', 'done')
    ordering = ('name',)

admin.site.register(Task, TaskAdmin)
