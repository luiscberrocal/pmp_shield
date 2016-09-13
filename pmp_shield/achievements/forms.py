from braces.forms import UserKwargModelFormMixin
from django import forms

from .models import Achievement


class AchievementForm(UserKwargModelFormMixin, forms.ModelForm):
    class Meta:
        model = Achievement  # , 'frequency',
        fields = ['employee', 'fiscal_year', 'type', 'description']
