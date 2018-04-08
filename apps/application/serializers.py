from rest_framework import serializers
from django.conf import settings

from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('github_username')

    def create(self, data):
        application = Application.objects.create(self.context.get("request").user, data['github_username'])
        application.save()
        return application
