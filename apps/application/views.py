from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view

from django.urls import reverse

from .serializers import ApplicationSerializer


@api_view(['GET'])
def home(request):
    return Response({
        reverse('application:home'): 'Information about application submission endpoints.',
        reverse('application:submit'): 'Submit a new application.'
    })


class ApplicationView(generics.CreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = (IsAuthenticated,)
