from django.contrib import admin
from reversion.admin import VersionAdmin
from website.apps.entry.models import Task, Content
from website.apps.core.admin import TrackedModelAdmin


class TaskAdmin(TrackedModelAdmin, VersionAdmin):
    date_hierarchy = 'added'
    list_display = ('name', 'source', 'form', 'added')
    list_filter = ('editor', 'source', 'form')
    ordering = ('name',)


class ContentAdmin(TrackedModelAdmin, VersionAdmin):
    date_hierarchy = 'added'
    list_filter = ('task', 'done')
    list_display = ('task', 'description', 'taskcomment', 'comment', 'done')
    ordering = ('added', 'task')
    search_fields = ('task', 'description', 'taskcomment', 'comment', 'done')


admin.site.register(Task, TaskAdmin)
admin.site.register(Content, ContentAdmin)
