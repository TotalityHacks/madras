from django.contrib import admin

from apps.reader import models

admin.site.register(models.Reader)
admin.site.register(models.Rating)
admin.site.register(models.RatingField)
admin.site.register(models.RatingResponse)
