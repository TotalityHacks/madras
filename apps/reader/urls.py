from django.conf.urls import url
from apps.reader import views

urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^rating/$', views.RatingView.as_view(), name="rating"),
    url(
        r'^next_application/$',
        views.NextApplicationView.as_view(),
        name="next_application",
    ),
    url(r'^skip/$', views.SkipView.as_view(), name="skip"),
    url(r'^stats/$', views.StatsView.as_view(), name="stats"),
]
