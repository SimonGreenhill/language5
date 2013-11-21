from django.contrib import admin
from reversion.admin import VersionAdmin
from website.apps.pronouns.models import Paradigm, Pronoun, Relationship
from website.apps.core.admin import TrackedModelAdmin


# Admin
class ParadigmAdmin(TrackedModelAdmin, VersionAdmin):
    date_hierarchy = 'added'
    list_display = ('language', 'source', 'analect', 'comment')
    list_filter = ('editor',)
    ordering = ('language',)
    search_fields = ('language', 'source', 'comment')


class PronounAdmin(TrackedModelAdmin, VersionAdmin):
    date_hierarchy = 'added'
    list_display = ('paradigm', 'pronountype', 'comment')
    list_filter = ('paradigm', 'pronountype')
    ordering = ('pronountype', )
    search_fields = ('paradigm', 'pronountype')


class RelationshipAdmin(TrackedModelAdmin, VersionAdmin):
    date_hierarchy = 'added'
    list_display = ('paradigm', 'pronoun1', 'pronoun2', 'relationship', 'comment')
    list_filter = ('paradigm', 'pronoun1', 'pronoun2', 'relationship')
    search_fields = ('paradigm', 'pronoun1', 'pronoun2', 'relationship', 'comment')


admin.site.register(Paradigm, ParadigmAdmin)
admin.site.register(Pronoun, PronounAdmin)
admin.site.register(Relationship, RelationshipAdmin)
