from django.conf.urls import url
from apps.reader import views

urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^rating/$', views.RatingView.as_view(), name="rating"),
    url(r'^next_application/$', views.NextApplication.as_view(), name="next_application"),
]
