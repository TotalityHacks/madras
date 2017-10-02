from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.stats.serializers import SummarySerializer

class Summary(APIView):    
    def get(self, request):
        return Response(
            SummarySerializer().to_representation(),
            status=status.HTTP_200_OK,
        )
