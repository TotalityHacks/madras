from django.conf.urls import url
from apps.locations.views import get_maps

urlpatterns = [
    url(r'', get_maps, name="get_maps")
]
