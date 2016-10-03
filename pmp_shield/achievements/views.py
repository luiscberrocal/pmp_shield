from braces.views import LoginRequiredMixin, UserFormKwargsMixin
from django import forms
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, CreateView, UpdateView

from .forms import AchievementForm
from ..employees.utils import employee_selection_util
from .models import Achievement


class AchievementListView(LoginRequiredMixin, UserFormKwargsMixin, ListView):
    model = Achievement
    context_object_name = 'achievements'

    def get_queryset(self):
        qs = super(AchievementListView, self).get_queryset()
        employee = employee_selection_util.get_current_employee(self.request)
        fiscal_year = int(self.kwargs['fiscal_year'])
        return qs.filter(employee=employee, fiscal_year=fiscal_year)


class AchievementCreateView(LoginRequiredMixin, UserFormKwargsMixin, CreateView):
    model = Achievement
    form_class = AchievementForm
    context_object_name = 'achievement'

    def get_initial(self):
        employee = employee_selection_util.get_current_employee(self.request)
        data = {'employee': employee,
                'fiscal_year': int(self.kwargs['fiscal_year'])}
        return data

    def get_success_url(self):
        data = self.get_initial()
        fiscal_year = data['fiscal_year']
        return reverse_lazy('achievements:achievement-list', kwargs={'fiscal_year': fiscal_year})


class AchievementUpdateView(LoginRequiredMixin, UserFormKwargsMixin, UpdateView):
    model = Achievement
    context_object_name = 'achievement'
    form_class = AchievementForm
