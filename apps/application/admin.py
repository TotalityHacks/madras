from django.contrib import admin

from .models import Application, Question, Answer

admin.site.register(Application)
admin.site.register(Question)
admin.site.register(Answer)
