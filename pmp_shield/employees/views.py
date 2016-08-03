from braces.views import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from .models import Employee


class EmployeeListView(LoginRequiredMixin, ListView):
    model = Employee

