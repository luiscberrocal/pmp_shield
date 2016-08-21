from django.conf.urls import url

from .views import EmployeeListView, EmployeeDetailView

urlpatterns = [
    url(r'^$', EmployeeListView.as_view(), name='employee-list'),
    url(r'^assigned/(?P<office_slug>[\w-]*)', EmployeeListView.as_view(), name='employee-list-assigned'),
    url(r'^assigned/(?P<office_slug>[\w-]*)/(?P<fiscal_year>\d{4})', EmployeeListView.as_view(),
        name='employee-list-assigned-fiscal-year'),
    url(r'^details/(?P<pk>[\d]*)', EmployeeDetailView.as_view(), name='employee-details'),
]
