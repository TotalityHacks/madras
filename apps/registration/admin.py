from django.contrib import admin

from apps.registration import models

admin.site.register(models.Application)
admin.site.register(models.Applicant)
