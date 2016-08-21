from braces.views import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from .models import Employee, OrganizationUnit


class EmployeeListView(LoginRequiredMixin, ListView):
    model = Employee

    def get_context_data(self, **kwargs):
        context = super(EmployeeListView, self).get_context_data(**kwargs)
        if self.kwargs.get('office_slug'):
            #office = OrganizationUnit.objects.get(slug=self.kwargs.get('office_slug'))
            context['title'] = 'Employees %s' % str(self.office)
        else:
            context['title'] = 'Employees'
        return context

    def get_queryset(self):
        qs = super(EmployeeListView, self).get_queryset()
        if self.kwargs.get('office_slug'):
            self.office = OrganizationUnit.objects.get(slug=self.kwargs.get('office_slug'))
            return Employee.objects.currently_assigned_to(self.office)
        else:
            return qs

