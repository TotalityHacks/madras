import csv
import uuid
from collections import OrderedDict

from rest_framework import generics, mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view

from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse

from .serializers import ApplicationSerializer, ResumeSerializer
from .services import load_questions
from .models import Application, Resume
from utils.upload import FileUploader


@api_view(['GET'])
def home(request):
    return Response(OrderedDict((
        (
            reverse('application:home'),
            'Information about application submission endpoints.'
        ),
        (
            reverse('application:save'),
            'Save a new, possibly incomplete, application.'),
        (
            reverse('application:submit'),
            'Submit a new application.'),
        (
            reverse('application:resume-list'),
            'Submit a resume for an application'
        ),
        (
            reverse('application:list_questions'),
            'List questions required for the application.'
        ),
    )))


SCHOOLS = list(school[0] for school in csv.reader(open("static/schools.csv")))


class ResumeViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):

    serializer_class = ResumeSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Resume.objects.all()

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        app = get_object_or_404(Application, user=self.request.user)
        file = serializer.validated_data['file']
        serializer.validated_data['id'] = uuid.uuid4()
        FileUploader().upload_file_to_s3(
            file,
            remote_filename=str(serializer.validated_data['id']),
        )
        serializer.save(application=app)

    def retrieve(self, request, pk):
        try:
            resume = get_object_or_404(Resume, id=uuid.UUID(pk))
        except ValueError:
            raise Http404

        resume_file = FileUploader().download_file_from_s3(str(resume.id))
        response = HttpResponse(resume_file, content_type="application/pdf")
        response['Content-Disposition'] = 'inline;filename=resume.pdf'
        return response


class ApplicationView(generics.ListCreateAPIView):
    """Create a new application. Pass in key value pairs in the form
    'question_X': ... where X is the ID of the question and ... is the answer.
    """
    serializer_class = ApplicationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Application.objects.filter(user=self.request.user)

    def list(self, request):
        try:
            app = Application.objects.get(user=request.user)
        except Application.DoesNotExist:
            return Response(
                {'error': 'No application has been submitted yet!'},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(ApplicationSerializer(app).data)


class QuestionListView(generics.ListAPIView):

    queryset = []

    def list(self, request):
        return Response(load_questions(), status=status.HTTP_200_OK)


@api_view(['GET'])
def get_schools_list(request):
    return Response({"schools": SCHOOLS})
