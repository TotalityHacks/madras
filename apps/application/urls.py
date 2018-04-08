from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^submit/', views.ApplicationView.as_view(), name='submit'),
]
