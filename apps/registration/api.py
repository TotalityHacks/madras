from rest_framework import generics, status, renderers, serializers
from rest_framework.compat import authenticate
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer as AuthTokenSerializerBase
from rest_framework.authtoken.views import ObtainAuthToken as ObtainAuthTokenBase
from rest_framework.views import APIView

from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .tokens import account_activation_token
from .serializers import UserSerializer
from .models import User


class UserRegistrationView(generics.CreateAPIView):
    """ Create a new user. If the associated email is a staff email address, create a staff user who is able to review applications. """

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

        return Response({
            "success": True,
            "message": "Account created! You will need to verify your email address before logging in."
        }, status=status.HTTP_201_CREATED)


class AuthTokenSerializer(AuthTokenSerializerBase):
    def validate(self, attrs):
        username = attrs.get('username') or attrs.get('email')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)

            if not user:
                if User.objects.filter(email=username).exists():
                    if not User.objects.get(email=username).is_active:
                        raise serializers.ValidationError('You cannot login until you have confirmed your email address.', code='authorization')
                raise serializers.ValidationError('Unable to login with provided credentials.', code='authorization')
        else:
            raise serializers.ValidationError('Must include "username" and "password".', code='authorization')

        attrs['user'] = user
        return attrs


class ObtainAuthToken(ObtainAuthTokenBase):
    """ Obtain an auth token used to make authorized requests to the API. """

    serializer_class = AuthTokenSerializer
    renderer_classes = (renderers.JSONRenderer, renderers.BrowsableAPIRenderer)


class Logout(APIView):
    """ Given an auth token, revoke the auth token and logout. """

    def get(self, request):
        if request.user.is_authenticated:
            if hasattr(request.user, "auth_token"):
                request.user.auth_token.delete()
        return Response({"success": True}, status=status.HTTP_200_OK)
