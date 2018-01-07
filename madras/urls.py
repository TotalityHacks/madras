"""madras URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from rest_framework.documentation import include_docs_urls
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    url(r'^docs/', include_docs_urls(title="Madras")),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^login/', obtain_auth_token),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^reader/', include('apps.reader.urls', namespace="reader")),
    url(r'^registration/', include('apps.registration.urls', namespace="registration")),
    url(r'^stats/', include('apps.stats.urls', namespace="stats")),
]
