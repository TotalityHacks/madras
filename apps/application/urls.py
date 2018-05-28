from rest_framework import routers

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^save/', views.ApplicationView.as_view(), name='save'),
    url(r'^submit/', views.ApplicationView.as_view(), name='submit'),
    url(
        r'^questions/$',
        views.QuestionListView.as_view(),
        name='list_questions',
    ),
    url(r'^schools_list/$', views.get_schools_list, name="schools_list"),
]

router = routers.DefaultRouter()
router.register(r'resumes', views.ResumeViewSet)
urlpatterns += router.urls
