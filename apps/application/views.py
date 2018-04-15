from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view

from django.urls import reverse

from .serializers import ApplicationSerializer, QuestionSerializer
from .models import Question


@api_view(['GET'])
def home(request):
    return Response({
        '/submit': 'Submit a new application',
    	'/questions': 'Gets the list of questions.',
    	'/questions/create': 'Creates a new question.',
    	'/questions/:id': 'Gets/updates/deletes the question with the specified ID.'
    })


class ApplicationView(generics.CreateAPIView):
    """ Create a new application. Pass in key value pairs in the form 'question_X': ... where X is the ID of the question and ... is the answer. """
    serializer_class = ApplicationSerializer
    permission_classes = (IsAuthenticated,)


class QuestionView(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    permission_classes = (IsAdminUser,)
    queryset = Question.objects.all()


class QuestionListView(generics.ListAPIView):
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Question.objects.all()
