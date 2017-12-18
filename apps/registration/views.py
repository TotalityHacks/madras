from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404

from apps.registration import models, serializers

class Application(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        applicant = get_object_or_404(models.Applicant, user=request.user)
        application = get_object_or_404(models.Application, applicant=applicant.application)

        return Response(
            serializers.ApplicationSchemaSerializer(application).data,
            status=status.HTTP_200_OK,
        )


class Applicant(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        applicant = get_object_or_404(models.Applicant, user=request.user)

        return Response(
            serializers.ApplicantSerializer(applicant).data,
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = serializers.ApplicantSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
