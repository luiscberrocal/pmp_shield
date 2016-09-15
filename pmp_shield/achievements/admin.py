from django.contrib import admin

# Register your models here.
from .models import Achievement


class AchievementAdmin(admin.ModelAdmin):
    list_display = ['employee', 'fiscal_year', 'type']


admin.site.register(Achievement, AchievementAdmin)
