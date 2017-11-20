import json
import random

from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.reader import serializers
from apps.reader.models import Applicant, RatingResponse


class Rating(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        rating = request.user.reader.hackathons.first().applications.first().rating

        return Response(
            serializers.RatingSchemaSerializer(rating).data,
            status=status.HTTP_200_OK,
        )

    def post(self, request):
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
        rand_pk = random.randint(0, Applicant.objects.all().count() - 1)
        rand_app = Applicant.objects.get(pk=rand_pk)
        return Response(
            {
                "applicant_id": rand_app.pk,
                "num_reads": RatingResponse.objects.filter(
                    applicant=rand_app).count(),
                "data": rand_app.data,
            },
            status=status.HTTP_200_OK,
        )
