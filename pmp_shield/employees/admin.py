from django.contrib import admin

# Register your models here.
from mptt.admin import MPTTModelAdmin

from .models import OrganizationUnit, Employee

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('company_id', 'last_name', 'first_name', 'office', 'photo_url')

admin.site.register(OrganizationUnit, MPTTModelAdmin)
admin.site.register(Employee, EmployeeAdmin)
