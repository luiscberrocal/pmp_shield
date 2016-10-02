from django.conf.urls import url

from .views import AchievementCreateView, AchievementListView, AchievementUpdateView

urlpatterns = [
    url(r'^create/(?P<fiscal_year>\d{4})/', AchievementCreateView.as_view(), name='achievement-create'),
    url(r'^update/(?P<pk>\d*)/', AchievementUpdateView.as_view(), name='achievement-update'),
    url(r'^list/(?P<fiscal_year>\d{4})/', AchievementListView.as_view(), name='achievement-list'),
    ]
