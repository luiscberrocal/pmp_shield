from django.conf.urls import url

from .views import EmployeeListView

urlpatterns = [
    url(r'^$', EmployeeListView.as_view(), name='employee-list'),
    url(r'^assigned/(?P<office_slug>[\w-]*)', EmployeeListView.as_view(), name='employee-list-assigned'),
]
