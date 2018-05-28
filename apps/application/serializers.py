from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnDict
from django.db import transaction
from django.urls import resolve

from .models import Application, Resume, Answer
from .services import get_question, load_questions


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = (
            'github_username', 'id', 'resumes', 'status', 'submission_date')
        read_only_fields = ('resumes', 'submission_date')

    status = serializers.CharField(source='get_status_display', read_only=True)

    def __init__(self, *args, **kwargs):
        super(ApplicationSerializer, self).__init__(*args, **kwargs)
        for question in load_questions():
            field_key = "question_{}".format(question["id"])
            self.fields[field_key] = serializers.CharField(
                help_text=question["text"], required=False)

    @property
    def data(self):
        data = super(serializers.ModelSerializer, self).data
        data["questions"] = {}
        if "id" in data:
            for answer in Answer.objects.filter(application=data["id"]):
                question_text = get_question(int(answer.question_id))["text"]
                data["questions"][question_text] = answer.text
        return ReturnDict(data, serializer=self)

    @transaction.atomic
    def create(self, data):
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
                Answer.objects.update_or_create(
                    question_id=question_id,
                    application=application,
                    defaults={'text': data[item]},
                )
                del self.fields[item]

        # do some basic field checking
        for question in load_questions():
            answer = Answer.objects.filter(
                question_id=question["id"], application=application)
            if answer.exists():
                answer = answer.first()
                # allow blank answers for saved applications (not submitted)
                if (
                    not answer.text and
                    not application.status == Application.SUBMITTED
                ):
                    continue
                if question["type"] == 'number':
                    if not answer.text.isdigit():
                        raise serializers.ValidationError(
                            '"{}" must be an integer value!'.format(
                                question["text"])
                        )

        # if app will be submitted, ensure that required fields are filled out
        if application.status == Application.SUBMITTED:
            for question in load_questions():
                if not question["required"]:
                    continue
                answer = Answer.objects.filter(
                    question_id=question["id"], application=application)
                if not answer.exists() or not answer.first().text:
                    raise serializers.ValidationError(
                        '"{}" is a required question!'.format(
                            question["text"])
                    )
        application.save()
        return application


class ResumeSerializer(serializers.ModelSerializer):

    file = serializers.FileField(write_only=True)

    class Meta:
        model = Resume
        fields = ('created_at', 'file', 'filename', 'id',)
        read_only_fields = ('created_at', 'id',)
        ordering = ('created_at',)

    def create(self, validated_data):
        validated_data.pop('file')
        return Resume.objects.create(**validated_data)
