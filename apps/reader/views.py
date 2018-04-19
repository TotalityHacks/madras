from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

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


class Rating(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        """Get the first rating of the first application of the first hackaton."""
        rating = request.user.given_ratings.first()

        return Response(serializers.RatingSchemaSerializer(rating).data)

    def post(self, request):
        """Add a rating to an applicant given an applicant ID."""
        params = dict(request.data)
        application_id = params.get("application_id")
        rating_number = params.get("user_rating")
        comments = params.get("comments")
        application = get_object_or_404(Application, id=application_id)
        RatingResponse.objects.create(
            reader=request.user,
            application=application,
            rating_number=rating_number,
            comments=comments
        )
        return Response({"detail": "success"})


class NextApplication(APIView):

    permission_classes = (IsAdminUser,)

    def get(self, request):
        """Get the next application that needs a review."""

        rand_app = Application.objects.annotate(reviews=Count('ratings')).filter(reviews__lt=settings.TOTAL_NUM_REVIEWS).first()
        github_array = get_metrics_github(rand_app.github_username)

        data = ApplicationSerializer(rand_app).data
        data.update(github_array)
        return Response(data)
