from rest_framework import serializers

from .models import Application, Question, Answer


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        exclude = ('user',)

    def validate_github_username(self, data):
        if Application.objects.filter(github_username=data).exists():
            raise serializers.ValidationError('An application with this GitHub username already exists!')

    def validate(self, data):
        if Application.objects.filter(user=self.context['request'].user).exists():
            raise serializers.ValidationError('You have already submitted an application for this hackathon!')

    def __init__(self, *args, **kwargs):
        super(ApplicationSerializer, self).__init__(*args, **kwargs)
        for question in Question.objects.all():
            self.fields["question_{}".format(question.id)] = serializers.CharField(help_text=question.text)

    def create(self, data):
        application = Application.objects.create(
            user=self.context['request'].user,
            github_username=data['github_username']
        )
        for item in data:
            if item.startwith("question_"):
                question_id = int(item.rsplit("_", 1)[-1])
                Answer.objects.create(question=question_id, application=application, text=data[item])
        application.save()
        return application


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'text')
        read_only_fields = ('id',)
