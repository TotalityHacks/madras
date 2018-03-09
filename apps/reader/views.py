import json
import random

from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.schemas import AutoSchema

from apps.reader import serializers
from apps.reader.models import Applicant, RatingResponse
from apps.reader.utils import get_metrics_github


class Rating(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """Get the first rating of the first application of the first hackaton."""
        rating = request.user.reader.hackathons.first().applications.first().rating

        return Response(
            serializers.RatingSchemaSerializer(rating).data,
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        """Add a rating to an applicant given an applicant ID."""
        params = dict(request.data)
        applicant_id = params.get("applicant_id")
        data = json.dumps(params)
        applicant = get_object_or_404(Applicant, pk=applicant_id)
        RatingResponse.objects.create(
            reader=request.user.reader, applicant=applicant, data=data)
        return Response({"detail": "success"}, status=status.HTTP_200_OK)


class NextApplication(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """Get the next application that needs a review."""

        rand_pk = random.randint(0, Applicant.objects.all().count() - 1)
        rand_app = Applicant.objects.get(pk=rand_pk)
        github_array = get_metrics_github(rand_app.github_user_name)
        return Response(
                {
                    "applicant_id": rand_app.pk,
                    "num_reads": RatingResponse.objects.filter(
                        applicant=rand_app).count(),
                    "data": rand_app.data,
                    "num_followers": github_array["NumFollowers"],
                    "num_repos": github_array["NumRepos"],
                    "num_contributions": github_array["NumContributions"],
                    "self_star_repos": github_array["selfStarRepos"]
                },
                status=status.HTTP_200_OK,
        )
