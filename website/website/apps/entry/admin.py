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
    list_filter = ('task', 'done', 'imported')
    list_display = ('task', 'description', 'taskcomment', 'comment', 'done', 'imported')
    ordering = ('added', 'task')
    search_fields = ('task', 'description', 'taskcomment', 'comment', 'done', 'imported')


admin.site.register(Task, TaskAdmin)
admin.site.register(Content, ContentAdmin)
