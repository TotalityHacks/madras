from django.conf.urls import url
from apps.announcements.views import announcements

urlpatterns = [
    url(r'', announcements, name="announcements"),
]
