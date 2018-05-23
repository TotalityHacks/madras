from django.conf.urls import url
from apps.checkin import views

urlpatterns = [
    url(r'^get_qr_code/$', views.GetQRCode.as_view(), name="get_qr_code"),
    url(r'^get_qr_code_admin/$', views.GetQRCodeAdmin.as_view(), name="get_qr_code_admin"),
    url(r'^check_in/$', views.CheckIn.as_view(), name="check_in"),
    url(r'^check_out/$', views.CheckOut.as_view(), name="check_out"),
]
