from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView

from apps.reader import serializers
from apps.reader.models import Rating, Skip
from apps.reader.utils import get_metrics_github
from apps.application.models import Application
from apps.application.serializers import SubmissionSerializer

from django.conf import settings
from django.urls import reverse
from django.db.models import Count, Sum, Case, When, IntegerField, BooleanField


@api_view(['GET'])
def home(request):
    """
    Endpoints for processing applications. These endpoints can only be
    accessed to users with the staff permission.
    """

    return Response({
        reverse("reader:rating"): 'Get given ratings and submit new ratings.',
        reverse("reader:next_application"): (
            'Get the next application to review.'),
        reverse("reader:stats"): 'Get reader statistics about the user',
        reverse("reader:skip"): 'Skips an application.',
    })


class RatingView(ListCreateAPIView):
    """
    Get all of the ratings given to all applications, or submit a new rating
    for an application.
    """
    serializer_class = serializers.RatingSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        return Rating.objects.all()


class NextApplicationView(APIView):

    permission_classes = (IsAdminUser,)

    def get(self, request):
        """Get the next application that needs a review."""

        rand_app = (
            Application.objects
            .annotate(
                reviews=Count('ratings'),
                submissions_count=Count('submissions'),
                skips=Sum(
                    Case(
                        When(skip__user=request.user, then=1),
                        default=0,
                        output_field=IntegerField(),
                    ),
                ),
                priority=Case(
                    When(created_at__lt=settings.PRIORITY_DEADLINE, then=True),
                    default=False,
                    output_field=BooleanField(),
                ),
            )
            .exclude(
                ratings__reader=request.user
            )
            .filter(
                reviews__lt=settings.TOTAL_NUM_REVIEWS,
                submissions_count__gt=0,
            )
            .order_by('priority', 'skips')
        ).first()

        if rand_app is None:
            return Response(
                {"error": "No more applications to review!"},
                status=status.HTTP_404_NOT_FOUND,
            )

        submission = rand_app.submissions.first()

        if submission.github:
            github_array = get_metrics_github(submission.github)
        else:
            github_array = {}

        data = SubmissionSerializer(submission).data
        data.update(github_array)
        return Response(data)


class SkipView(ListCreateAPIView):
    """
    List all applications marked as skipped for the current user or skip an
    application, which makes it not appear when the user requests additional
    applications to review.
    """
    serializer_class = serializers.SkipSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        return Skip.objects.all()


class StatsView(APIView):

    permission_classes = (IsAdminUser,)

    def get(self, request):
        return Response({
            "num_reads": request.user.given_ratings.all().count(),
        })
