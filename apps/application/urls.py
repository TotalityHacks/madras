from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^submit/', views.ApplicationView.as_view(), name='submit'),
    url(r'^questions/$', views.QuestionView.as_view({'get': 'list'})),
    url(r'^questions/(?P<pk>[0-9]+)/$', views.QuestionView.as_view({
        'get': 'retrieve',
        'post': 'create',
        'put': 'update',
        'delete': 'destroy'
    }), name='question'),
]
