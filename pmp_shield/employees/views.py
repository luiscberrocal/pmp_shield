from braces.views import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView

from .models import Employee, OrganizationUnit


class EmployeeListView(LoginRequiredMixin, ListView):
    model = Employee

    def get_context_data(self, **kwargs):
        context = super(EmployeeListView, self).get_context_data(**kwargs)
        if self.office:
            #office = OrganizationUnit.objects.get(slug=self.kwargs.get('office_slug'))
            context['title'] = 'Employees %s' % str(self.office)
        else:
            context['title'] = 'Employees'
        return context

    def get_queryset(self):
        qs = super(EmployeeListView, self).get_queryset()
        if self.kwargs.get('office_slug'):
            try:
                self.office = OrganizationUnit.objects.get(slug=self.kwargs.get('office_slug'))
                if self.kwargs.get('fiscal_year'):
                    year = int(self.kwargs['fiscal_year'])
                    return Employee.objects.assigned_on_fiscal_year_to(year, self.office)
                else:
                    return Employee.objects.currently_assigned_to(self.office)
            except OrganizationUnit.DoesNotExist:
                self.office = None
                return None
        else:
            return qs

class EmployeeDetailView(LoginRequiredMixin, DetailView):
    model = Employee
    context_object_name = 'employee'
