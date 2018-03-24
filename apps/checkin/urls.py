from django.conf.urls import url
from apps.checkin import views

urlpatterns = [
    url(r'^gen_qr_code/$', views.gen_qr_code, name="gen_qr_code"),
]
