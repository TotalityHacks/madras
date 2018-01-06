from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class Summary(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        hackathon = request.user.reader.hackathons.first()
        total_reads = 0
        for applicant in hackathon.applicants.all():
            total_reads += applicant.ratings.all().count()
        return Response({
            "num_applicants": hackathon.applicants.all().count(),
            "num_total_reads": total_reads,
        }, status=status.HTTP_200_OK)


class Leaderboard(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        hackathon = request.user.reader.hackathons.first()
        readers = list(hackathon.readers.all())
        readers = reversed(sorted(readers, key=lambda r: r.ratings.all().count()))
        return Response({
            "results": [{"name": r.user.username, "num_reads": r.ratings.all().count()} for r in readers],
        }, status=status.HTTP_200_OK)
