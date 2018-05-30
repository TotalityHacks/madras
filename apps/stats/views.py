from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.urls import reverse
from ..application.models import Application, Submission
from ..reader.models import Rating
from ..registration.models import User


@api_view(['GET'])
def home(request):
    """ Statistics for ratings and applications. """

    return Response({
        reverse("stats:summary"): (
            'Summary information about reviews done by the current reviewer.'),
        reverse("stats:leaderboard"): (
            'Information about overall applications and readers.'),
    })


class Summary(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        num_submitted = len(set(
            Submission.objects.all().values_list("application_id", flat=True)))
        return Response({
            "num_applicants": Application.objects.all().count(),
            "num_submitted_applications": num_submitted,
            "num_total_reads": Rating.objects.all().count(),
        }, status=status.HTTP_200_OK)


class Leaderboard(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        readers = list(User.objects.filter(is_staff=True))
        readers = reversed(
            sorted(readers, key=lambda r: r.given_ratings.all().count()))
        return Response({
            "results": [{
                "name": r.username,
                "num_reads": r.given_ratings.all().count(),
            } for r in readers],
        }, status=status.HTTP_200_OK)
