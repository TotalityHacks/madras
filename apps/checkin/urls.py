from django.conf.urls import url
from apps.checkin import views

urlpatterns = [
    url(r'^get_qr_code/$', views.GetQRCode.as_view(), name="get_qr_code"),
    # url(r'^get_qr_codes/$', views.get_qr_codes, name="get_qr_codes"),
    url(r'^check_in/$', views.check_in, name="check_in"),
    url(r'^check_out/$', views.check_out, name="check_out"),
]
