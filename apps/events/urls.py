from django.conf.urls import url
from apps.events.views import get_events

urlpatterns = [
    url(r'', get_events, name="get_events"),
]
