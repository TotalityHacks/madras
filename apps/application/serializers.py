from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnDict
from django.db import transaction
from django.urls import resolve

from .models import Application, Question, Resume, Answer, Choice


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('github_username', 'id', 'resumes', 'status', 'submission_date')
        read_only_fields = ('resumes', 'submission_date')

    status = serializers.CharField(source='get_status_display', read_only=True)

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
            request = self.context['request']
            user = request.user
            current_url = resolve(request.path_info).url_name
            existing = Application.objects.filter(user=user)
            if existing.exists():
                existing.update(
                    github_username=data['github_username']
                )
                application = existing.first()
            else:
                application = Application.objects.create(
                    user=user,
                    github_username=data['github_username']
                )
            if current_url == 'save':
                if not application.status == Application.SUBMITTED:
                    application.status = Application.SAVED
            else:
                application.status = Application.SUBMITTED
            for item in data:
                if item.startswith("question_"):
                    question_id = int(item.rsplit("_", 1)[-1])
                    question = Question.objects.get(id=question_id)
                    Answer.objects.update_or_create(question=question, application=application, defaults={'text': data[item]})
                    del self.fields[item]

            # do some basic field checking
            for question in Question.objects.all():
                answer = Answer.objects.filter(question=question, application=application)
                if answer.exists():
                    answer = answer.first()
                    if question.type == 'number':
                        if not answer.text.isdigit():
                            raise serializers.ValidationError('"{}" must be an integer value!'.format(question.text))
                    elif question.type == 'choice':
                        if not Choice.objects.filter(question=question, value=answer.text).exists():
                            raise serializers.ValidationError('"{}" must be one of the predetermined choices!'.format(question.text))

            # if application will be submitted, ensure that required fields are filled out
            if application.status == Application.SUBMITTED:
                for question in Question.objects.filter(required=True):
                    answer = Answer.objects.filter(question=question, application=application)
                    if not answer.exists() or not answer.first().text:
                        raise serializers.ValidationError('"{}" is a required question!'.format(question.text))
            application.save()
        return application


class ResumeSerializer(serializers.ModelSerializer):

    file = serializers.FileField(write_only=True)

    class Meta:
        model = Resume
        fields = ('created_at', 'file', 'filename', 'id',)
        read_only_fields = ('created_at', 'id',)

    def create(self, validated_data):
        validated_data.pop('file')
        return Resume.objects.create(**validated_data)


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'type', 'max_length', 'prefix', 'text', 'required', 'choices')
        read_only_fields = ('id', 'choices')


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('id', 'question', 'value')
        read_only_fields = ('id',)
