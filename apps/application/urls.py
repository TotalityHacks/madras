from rest_framework import routers

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^questions/$', views.get_questions_list, name='questions-list'),
    url(r'^schools_list/$', views.get_schools_list, name="schools-list"),
]

router = routers.DefaultRouter()
router.register(
    r'application', views.ApplicationViewSet, base_name="application")
router.register(r'resumes', views.ResumeViewSet, base_name="resume")
router.register(
    r'submissions', views.SubmissionViewSet, base_name="submissions")
urlpatterns += router.urls
