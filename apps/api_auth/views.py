from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class Login(APIView):    
    def post(self, request):
        return Response({"token": "abc-123"}, status=status.HTTP_200_OK)


class Logout(APIView):
    def post(self, request):
        return Response({"detail": "success"}, status=status.HTTP_200_OK)
