import csv
import uuid
from collections import OrderedDict

from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view

from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse

from . import serializers
from .models import Application, Resume, Submission
from utils.upload import FileUploader
from utils.email import send_template_email
from utils.slack import send_to_slack

from botocore.exceptions import ClientError


@api_view(['GET'])
def home(request):
    return Response(OrderedDict((
        (
            reverse('application:home'),
            'Information about application submission endpoints.'
        ),
        (
            reverse('application:application-list'),
            'Load and update an in-progress application'
        ),
        (
            reverse('application:resume-list'),
            'Submit a resume for an application'
        ),
        (
            reverse('application:submission-list'),
            'Submit an application'
        ),
    )))


class ResumeViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):

    serializer_class = serializers.ResumeSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        file = serializer.validated_data['file']
        serializer.validated_data['id'] = uuid.uuid4()
        if not settings.DEBUG:
            FileUploader().upload_file_to_s3(
                file,
                remote_filename=str(serializer.validated_data['id']),
            )
        serializer.save(user=self.request.user)

    def retrieve(self, request, pk):
        try:
            resume = get_object_or_404(Resume, id=uuid.UUID(pk))
        except ValueError:
            raise Http404
        if not settings.DEBUG:
            try:
                resume_file = FileUploader().download_file_from_s3(
                    str(resume.id)
                    )
            except ClientError:
                raise Http404
        else:
            resume_file = "dummy"
        response = HttpResponse(resume_file, content_type="application/pdf")
        response['Content-Disposition'] = (
            "inline;filename={}.pdf".format(uuid.uuid4()))
        response['X-Frame-Options'] = '*'
        return response


class ApplicationViewSet(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         viewsets.GenericViewSet):

    serializer_class = serializers.ApplicationSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        app, _ = Application.objects.get_or_create(user=request.user)
        if request.method == 'GET':
            return Response(
                serializers.ApplicationSerializer(app).data,
                status=status.HTTP_200_OK,
            )
        else:
            return Response("wow")

    def get_queryset(self):
        return Application.objects.filter(user=self.request.user)


class SubmissionViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):

    serializer_class = serializers.SubmissionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Submission.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        app, _ = Application.objects.get_or_create(user=self.request.user)

        if not app.submissions.exists() and settings.SLACK_TOKEN:
            send_to_slack(
                ":tada: New application submission! {} :tada:"
                .format(self.request.user.username),
                settings.SLACK_TOKEN,
                settings.SLACK_CHANNEL,
            )

        serializer.save(application=app, user=self.request.user)

        # send confirmation email to user
        user = self.request.user
        subject = 'Application Submitted!'
        send_template_email(user.email, subject, 'app_submitted.html', {})


@api_view(['GET'])
def get_schools_list(request):
    schools = list(
        school[0] for school in csv.reader(open("static/schools.csv")))
    return Response({"schools": schools})
