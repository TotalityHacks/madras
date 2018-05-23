from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^save/', views.ApplicationView.as_view(), name='save'),
    url(r'^submit/', views.ApplicationView.as_view(), name='submit'),
    url(r'^resume/', views.ResumeView.as_view(), name='upload_resume'),
    url(r'^questions/$', views.QuestionListView.as_view(), name='list_questions'),
    url(r'^questions/create$', views.QuestionView.as_view({'post': 'create'}), name='create_question'),
    url(r'^questions/(?P<pk>[0-9]+)/$', views.QuestionView.as_view({
        'get': 'retrieve',
        'post': 'update',
        'delete': 'destroy'
    }), name='question'),
    url(r'^schools_list/$', views.get_schools_list, name="schools_list"),
]
