from django.contrib import admin
from django.db.models import Count
from reversion.admin import VersionAdmin
from website.apps.lexicon.models import Lexicon
from website.apps.entry.models import Task, TaskLog, Wordlist, WordlistMember
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
    list_display = ('id', 'name', 'records', 'view', 'added', 'completable', 'done')
    list_filter = ('editor', 'done', 'completable', CheckpointListFilter, 'source', 'language', 'view')
    ordering = ('name',)
    exclude = ('lexicon',)
    list_select_related = True
    

class TaskLogAdmin(admin.ModelAdmin):
    date_hierarchy = 'time'
    list_display = ('person', 'task_id', 'time', 'page', 'message')
    list_filter = ('person', 'page', )
    ordering = ('-time',)
    list_select_related = True
    
    def task_id(self, instance):
        return instance.task_id
            
            
class WordlistMembersInline(admin.TabularInline):
    model = Wordlist.words.through
    extra = 0 # don't add anything new unless explicitly told to.


class TaskWordlistAdmin(TrackedModelAdmin, VersionAdmin):
    date_hierarchy = 'added'
    list_display = ('id', 'name', 'words_count')
    ordering = ('name',)
    filter_horizontal = ('words',)
    inlines = [WordlistMembersInline,]
    
    def queryset(self, request):
        return Wordlist.objects.annotate(words_count=Count("words"))
        
    def words_count(self, inst):
        return inst.words_count
    words_count.admin_order_field = 'words_count'


admin.site.register(Task, TaskAdmin)
admin.site.register(TaskLog, TaskLogAdmin)
admin.site.register(Wordlist, TaskWordlistAdmin)


