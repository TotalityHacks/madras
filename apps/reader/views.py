from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView

from apps.reader import serializers
from apps.reader.models import RatingResponse
from apps.reader.utils import get_metrics_github
from apps.application.models import Application

from django.conf import settings
from django.urls import reverse
from django.db.models import Count

from ..application.serializers import ApplicationSerializer


@api_view(['GET'])
def home(request):
    """ Endpoints for processing applications. These endpoints can only be accessed to users with the staff permission. """

    return Response({
        reverse("reader:rating"): 'Get given ratings and submit new ratings.',
        reverse("reader:next_application"): 'Get the next application to review.'
    })


class Rating(ListCreateAPIView):
    """ Get all of the ratings given to all applications, or submit a new rating for an application. """
    serializer_class = serializers.RatingResponseSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        return RatingResponse.objects.all()


class NextApplication(APIView):

    permission_classes = (IsAdminUser,)

    def get(self, request):
        """Get the next application that needs a review."""

        rand_app = Application.objects.annotate(reviews=Count('ratings')).filter(reviews__lt=settings.TOTAL_NUM_REVIEWS).first()
        github_array = get_metrics_github(rand_app.github_username)

        data = ApplicationSerializer(rand_app).data
        data.update(github_array)
        return Response(data)
