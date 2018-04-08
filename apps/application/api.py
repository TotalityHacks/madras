from rest_framework import generics, status, renderers
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken as ObtainAuthTokenBase

from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .tokens import account_activation_token
from .serializers import ApplicationSerializer


class ApplicationView(generics.CreateAPIView):
    serializer_class = ApplicationSerializer

    def create(self, request):
        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            application = serializer.create(request.data)
        else:
            return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"success": True}, status=status.HTTP_201_CREATED)

