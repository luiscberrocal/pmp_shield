from braces.views import LoginRequiredMixin, UserFormKwargsMixin
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, CreateView

from .forms import AchievementForm
from ..employees.utils import employee_selection_util
from .models import Achievement


class AchievementListView(LoginRequiredMixin, UserFormKwargsMixin, ListView):
    model = Achievement
    context_object_name = 'achievements'

    def get_queryset(self):
        qs = super(AchievementListView, self).get_queryset()
        employee = employee_selection_util.get_current_employee(self.request)
        return qs.filter(employee=employee)


class AchievementCreateView(LoginRequiredMixin, UserFormKwargsMixin, CreateView):
    model = Achievement
    form_class = AchievementForm

    def get_initial(self):
        employee = employee_selection_util.get_current_employee(self.request)
        data = {'employee': employee,
                'fiscal_year': int(self.kwargs['fiscal_year'])}
        return data

