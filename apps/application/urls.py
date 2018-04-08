from django.conf.urls import url

from . import api

urlpatterns = [
    url(r'^submit/$', api.ApplicationView.as_view(), name='submit'),
]
