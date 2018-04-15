from rest_framework import serializers

from .models import Application, Question


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('github_username',)

    def validate_github_username(self, data):
        if Application.objects.filter(github_username=data).exists():
            raise serializers.ValidationError('An application with this GitHub username already exists!')

    def validate(self, data):
        if Application.objects.filter(user=self.context['request'].user).exists():
            raise serializers.ValidationError('You have already submitted an application for this hackathon!')

    def create(self, data):
        application = Application.objects.create(
            user=self.context['request'].user,
            github_username=data['github_username']
        )
        application.save()
        return application


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('text',)
