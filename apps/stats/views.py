from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from apps.stats.serializers import SummarySerializer, LeaderboardSerializer

class Summary(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response(
            SummarySerializer().to_representation(),
            status=status.HTTP_200_OK,
        )


class Leaderboard(APIView):
    permission_classes = (IsAuthenticated,)
 
    def get(self, request):
        return Response(
            LeaderboardSerializer().to_representation(),
            status=status.HTTP_200_OK,
        )
