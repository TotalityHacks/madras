from rest_framework import serializers
from django.conf import settings

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'github_username')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def validate_password(self, value):
        for validator in settings.AUTH_PASSWORD_VALIDATORS:
            cls = validator['NAME'].rsplit(".", 1)[-1]
            method = getattr(__import__(validator['NAME'].rsplit(".", 1)[0], fromlist=[cls]), cls)
            method().validate(password=value)

    def create(self, data):
        user = User.objects.create_user(data['email'], data['password'], github_username=data.get('github_username') or None)
        user.is_active = False
        user.save()
        return user
