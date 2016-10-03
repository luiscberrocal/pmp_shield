from auditlog.models import LogEntry
from django.contrib import admin

# Register your models here.
from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _
from .models import Project, Assumption, Restriction, Milestone

class OfficeFilter(SimpleListFilter):
    title = _('executing_office') # or use _('country') for translated title
    parameter_name = 'executing_office'

    def lookups(self, request, model_admin):
        offices = set([c.executing_office for c in model_admin.model.objects.all()])
        if list(offices)[0] is None:
            return None
        else:
            return [(c.id, c.short_name) for c in offices]
        # You can also use hardcoded model name like "Country" instead of
        # "model_admin.model" if this is not direct foreign key filter

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(office__id__exact=self.value())
        else:
            return queryset

class MilestoneInline(admin.TabularInline):
    model = Milestone

    def get_extra(self, request, obj=None, **kwargs):
        extra = 3
        if obj:
            return 1
        return extra


class ProjectAdmin(admin.ModelAdmin):

    list_display = ('name', 'executing_office', 'sponsor', 'project_manager')
    list_filter = (OfficeFilter,)
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
