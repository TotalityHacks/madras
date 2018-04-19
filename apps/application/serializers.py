from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnDict
from django.db import transaction

from .models import Application, Question, Answer


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(ApplicationSerializer, self).__init__(*args, **kwargs)
        for question in Question.objects.all():
            self.fields["question_{}".format(question.id)] = serializers.CharField(help_text=question.text, required=False)

    @property
    def data(self):
        data = super(serializers.ModelSerializer, self).data
        data["questions"] = []
        if "id" in data:
            for answer in Answer.objects.filter(application=data["id"]):
                data["questions"].append([answer.question.text, answer.text])
        return ReturnDict(data, serializer=self)

    def create(self, data):
        with transaction.atomic():
            user = self.context['request'].user
            Application.objects.filter(user=user).delete()
            application = Application.objects.create(
                user=user,
                github_username=data['github_username']
            )
            for item in data:
                if item.startswith("question_"):
                    question_id = int(item.rsplit("_", 1)[-1])
                    question = Question.objects.get(id=question_id)
                    Answer.objects.create(question=question, application=application, text=data[item])
                    del self.fields[item]
            application.save()
        return application


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'type', 'text')
        read_only_fields = ('id',)
