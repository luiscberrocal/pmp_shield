from django.contrib import admin

# Register your models here.
from .models import Position, PositionDescription


class PositionAdmin(admin.ModelAdmin):
    list_display = ('grade', 'number', 'tenure', 'position_description', 'current_owner', 'current_office')

class PositionDescriptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name')



admin.site.register(Position, PositionAdmin)
admin.site.register(PositionDescription, PositionDescriptionAdmin)
