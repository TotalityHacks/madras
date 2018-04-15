from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^submit/', views.ApplicationView.as_view(), name='submit'),
    url(r'^questions/$', views.QuestionListView.as_view()),
    url(r'^questions/create$', views.QuestionView.as_view({'post': 'create'})),
    url(r'^questions/(?P<pk>[0-9]+)/$', views.QuestionView.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    }), name='question'),
]
