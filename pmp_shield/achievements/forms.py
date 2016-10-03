from braces.forms import UserKwargModelFormMixin
from django import forms

from .models import Achievement


class AchievementForm(UserKwargModelFormMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AchievementForm, self).__init__(*args, **kwargs)
        self.fields['employee'].widget = forms.HiddenInput()
        self.fields['fiscal_year'].widget = forms.HiddenInput()

    class Meta:
        model = Achievement  # , 'frequency',
        fields = ['employee', 'fiscal_year', 'type', 'description']


