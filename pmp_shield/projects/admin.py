from auditlog.models import LogEntry
from django.contrib import admin

# Register your models here.
from .models import Project, Assumption, Restriction, Milestone

class MilestoneInline(admin.TabularInline):
    model = Milestone

    def get_extra(self, request, obj=None, **kwargs):
        extra = 3
        if obj:
            return 1
        return extra


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'sponsor', 'project_manager')
    inlines = [
        MilestoneInline,
    ]


class AssumptionAdmin(admin.ModelAdmin):
    list_display = ('project', 'display_order', 'name', 'description')

class RestrictionAdmin(admin.ModelAdmin):
    list_display = ('project', 'display_order', 'name', 'description')

class MilestioneAdmin(admin.ModelAdmin):
    list_display = ('project', 'date', 'milestone_type', 'name')

class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'action', 'object_repr', 'object_pk', 'timestamp', 'actor')
    list_filter = ('content_type', 'action',)

admin.site.register(Project, ProjectAdmin)
admin.site.register(Assumption, AssumptionAdmin)
admin.site.register(Restriction, RestrictionAdmin)
admin.site.register(Milestone, MilestioneAdmin)

#admin.site.register(LogEntry, LogEntryAdmin)
