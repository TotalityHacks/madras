from django.conf.urls import url
from apps.registration import views

urlpatterns = [
    url(r'^application/$', views.Application.as_view(), name="application"),
    url(r'^applicant/$', views.Applicant.as_view(), name="applicant"),
]
