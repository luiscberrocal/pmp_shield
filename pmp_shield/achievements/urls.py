from django.conf.urls import url

from .views import AchievementCreateView

urlpatterns = [
    url(r'^create/(?P<fiscal_year>\d{4})/', AchievementCreateView.as_view(), name='achievement-create'),
    ]
