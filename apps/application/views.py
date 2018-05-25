import csv
import uuid
from collections import OrderedDict

from rest_framework import status
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view

from django.shortcuts import get_object_or_404
from django.urls import reverse

from .serializers import ApplicationSerializer, QuestionSerializer, ResumeSerializer, ChoiceSerializer
from .models import Question, Application, Choice
from utils.upload import FileUploader


@api_view(['GET'])
def home(request):
    return Response(OrderedDict((
        (reverse('application:home'), 'Information about application submission endpoints.'),
        (reverse('application:save'), 'Save a new, possibly incomplete, application.'),
        (reverse('application:submit'), 'Submit a new application.'),
        (reverse('application:upload_resume'), 'Submit a resume for an application'),
        (reverse('application:list_questions'), 'List questions required for the application.'),
        (reverse('application:create_question'), 'Create a new application question.'),
        (reverse('application:question', kwargs={'pk': 1234}), 'Get, modify, and delete questions.'),
        (reverse('application:list_choices'), 'List all choices associated with questions.'),
        (reverse('application:create_choice'), 'Create a new choice associated with a question.'),
        (reverse('application:choice', kwargs={'pk': 1234}), 'Get, modify, and delete choices.'),
    )))


SCHOOLS = list(school[0] for school in csv.reader(open("static/schools.csv")))


class ResumeView(generics.CreateAPIView):

    serializer_class = ResumeSerializer
    permission_classes = (IsAuthenticated,)

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


class ApplicationView(generics.ListCreateAPIView):
    """ Create a new application. Pass in key value pairs in the form 'question_X': ... where X is the ID of the question and ... is the answer. """
    serializer_class = ApplicationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Application.objects.filter(user=self.request.user)

    def list(self, request):
        try:
            app = Application.objects.get(user=request.user)
        except Application.DoesNotExist:
            return Response({'error': 'No application has been submitted yet!'}, status=status.HTTP_404_NOT_FOUND)
        return Response(ApplicationSerializer(app).data)


class QuestionView(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    permission_classes = (IsAdminUser,)
    queryset = Question.objects.all()


class QuestionListView(generics.ListAPIView):
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Question.objects.all()


@api_view(['GET'])
def get_schools_list(request):
    return Response({"schools": SCHOOLS})


class ChoiceView(viewsets.ModelViewSet):
    serializer_class = ChoiceSerializer
    permission_classes = (IsAdminUser,)
    queryset = Choice.objects.all()


class ChoiceListView(generics.ListAPIView):
    serializer_class = ChoiceSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Choice.objects.all()
