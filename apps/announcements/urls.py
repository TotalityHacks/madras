from django.conf.urls import url
from apps.announcements.views import get_announcements

urlpatterns = [
    url(r'', get_announcements, name="get_announcements")
]
