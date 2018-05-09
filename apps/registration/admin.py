from django.contrib import admin

from . import models


class UserAdmin(admin.ModelAdmin):
    search_fields = ('email',)
    list_display = ('email', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser')


admin.site.register(models.User, UserAdmin)
