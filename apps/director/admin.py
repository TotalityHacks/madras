from django.contrib import admin

from apps.director import models

admin.site.register(models.Organization)
admin.site.register(models.Hackathon)
