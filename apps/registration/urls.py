from django.conf.urls import url

from . import views
from . import api

TOKEN_REGEX = (
    r'(?P<uidb64>[0-9A-Za-z_\-]+)/'
    r'(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$'
)


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^signup/$', api.UserRegistrationView.as_view(), name='signup'),
    url(r'^reset/$', api.PasswordResetView.as_view(), name='reset'),
    url(
        r'^resend_email/$',
        api.ResendConfirmationView.as_view(),
        name='resend_email',
    ),
    url(r'^activate/' + TOKEN_REGEX, views.activate, name='activate'),
    url(r'recover/' + TOKEN_REGEX, views.recover, name='recover'),
]
