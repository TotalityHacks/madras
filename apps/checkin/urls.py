from django.conf.urls import url
from apps.checkin import views

urlpatterns = [
    url(r'^get_qr_code/$', views.get_qr_code, name="get_qr_code"),
    url(r'^get_qr_codes/$', views.get_qr_codes, name="get_qr_codes"),
]
