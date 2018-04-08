from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import ApplicationSerializer


class ApplicationView(generics.CreateAPIView):
    serializer_class = ApplicationSerializer

    def create(self, request):
        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(request.data)
        else:
            return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"success": True}, status=status.HTTP_201_CREATED)
