from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.reader import serializers
from apps.reader.models import Applicant, RatingResponse
from apps.reader.utils import get_metrics_github

from django.conf import settings
from django.db.models import Count


class Rating(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """Get the first rating of the first application of the first hackaton."""
        rating = request.user.reader.hackathons.first().applications.first().rating

        return Response(serializers.RatingSchemaSerializer(rating).data)

    def post(self, request):
        """Add a rating to an applicant given an applicant ID."""
        params = dict(request.data)
        applicant_id = params.get("applicant_id")
        rating_number = params.get("user_rating")
        comments = params.get("comments")
        applicant = get_object_or_404(Applicant, pk=applicant_id)
        RatingResponse.objects.create(
            reader=request.user.reader, applicant=applicant, rating_number=rating_number,
            comments=comments)
        return Response({"detail": "success"})


class NextApplication(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """Get the next application that needs a review."""

        rand_app = Applicant.objects.annotate(reviews=Count('ratings')).filter(reviews__lt=settings.TOTAL_NUM_REVIEWS).first()
        github_array = get_metrics_github(rand_app.github_user_name)

        return Response({
            "applicant_id": rand_app.pk,
            "num_reads": RatingResponse.objects.filter(
                applicant=rand_app).count(),
            "num_followers": github_array["num_followers"],
            "num_repos": github_array["num_repos"],
            "num_contributions": github_array["num_contributions"],
            "self_star_repos": github_array["self_star_repos"]
        })
