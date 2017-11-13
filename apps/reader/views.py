import json
import random

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.reader import serializers
from apps.reader.models import Applicant


class Rating(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        rating = request.user.reader.hackathons.first().applications.first().rating

        return Response(
            serializers.RatingSchemaSerializer(rating).data,
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        return Response({"detail": "success"}, status=status.HTTP_200_OK)


class NextApplication(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        rand_app = Applicant.objects.all()[random.randint(0, Applicant.objects.all().count() - 1)]
        return Response(
            {
                "applicant_id": rand_app.pk,
                "num_reads": random.randint(1, 10),
                "data": rand_app.data,
            },
            status=status.HTTP_200_OK,
        )
