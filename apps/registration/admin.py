from django.contrib import admin

from . import models

admin.site.register(models.Application)
admin.site.register(models.User)
