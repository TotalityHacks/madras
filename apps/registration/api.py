from rest_framework import generics, status, renderers
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken as ObtainAuthTokenBase

from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .tokens import account_activation_token
from .serializers import UserSerializer


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.create(request.data)
        else:
            return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        # send activation email to user
        current_site = get_current_site(request)
        message = render_to_string('acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        mail_subject = 'Activate your account!'
        to_email = user.email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()

        return Response({"success": True}, status=status.HTTP_201_CREATED)


class ObtainAuthToken(ObtainAuthTokenBase):
    renderer_classes = (renderers.JSONRenderer, renderers.BrowsableAPIRenderer)
