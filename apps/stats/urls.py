from django.conf.urls import url
from apps.stats import views

urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^summary/$', views.Summary.as_view(), name="summary"),
    url(r'^leaderboard/$', views.Leaderboard.as_view(), name="leaderboard"),
]
