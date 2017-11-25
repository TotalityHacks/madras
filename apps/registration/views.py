from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.registration import serializers

class Application(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        application = request.user.applicant.application

        return Response(
            serializers.ApplicationSchemaSerializer(application).data,
            status=status.HTTP_200_OK,
        )
