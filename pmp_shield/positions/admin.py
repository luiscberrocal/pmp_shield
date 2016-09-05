from django.contrib import admin

# Register your models here.
from .models import Position


class PositionAdmin(admin.ModelAdmin):
    list_display = ('grade', 'number', 'tenure', 'position_description', 'current_owner', 'current_office')


admin.site.register(Position, PositionAdmin)
