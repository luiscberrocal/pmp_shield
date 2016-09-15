from django.contrib import admin

# Register your models here.
from django.contrib.admin import SimpleListFilter
from mptt.admin import MPTTModelAdmin
from django.utils.translation import ugettext_lazy as _
from .models import OrganizationUnit, Employee, UnitAssignment


class OfficeFilter(SimpleListFilter):
    title = _('office') # or use _('country') for translated title
    parameter_name = 'office'

    def lookups(self, request, model_admin):
        offices = set([c.office for c in model_admin.model.objects.all()])
        if len(offices) == 0 or list(offices)[0] is None:
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

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('company_id', 'last_name', 'first_name', 'office',)
    list_filter = (OfficeFilter,)

class UnitAssingmentAdmin(admin.ModelAdmin):
    list_display = ('employee', 'office', 'start_date', 'end_date')
    list_filter = (OfficeFilter,)

admin.site.register(OrganizationUnit, MPTTModelAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(UnitAssignment, UnitAssingmentAdmin)
