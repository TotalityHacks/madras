from rest_framework import generics, status, renderers, serializers
from rest_framework.authtoken.models import Token
from rest_framework.compat import authenticate
from rest_framework.response import Response
from rest_framework.authtoken.serializers import (
    AuthTokenSerializer as AuthTokenSerializerBase)
from rest_framework.authtoken.views import (
    ObtainAuthToken as ObtainAuthTokenBase)
from rest_framework.views import APIView

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .tokens import account_activation_token
from .serializers import UserSerializer, PasswordResetSerializer
from .models import User

from utils.slack import send_to_slack
from utils.email import send_template_email


class UserRegistrationView(generics.CreateAPIView):
    """
    Create a new user. If the associated email is a staff email address,
    create a staff user who is able to review applications.
    """

    serializer_class = UserSerializer

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.create(request.data)
        else:
            return Response(
                {"success": False, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        current_site = get_current_site(request)
        send_template_email(
            user.email,
            'Activate your account!',
            'acc_active_email.html',
            {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

        # send intro email
        send_template_email(
                user.email,
                'Thanks for applying!',
                'intro_email.html',
                {},
                settings.INTRO_EMAIL_FROM,
                settings.INTRO_EMAIL_DELAY
            )

        # notify the slack channel
        if settings.SLACK_TOKEN:
            send_to_slack(
                "A new user {} just made an account!".format(user.username),
                settings.SLACK_TOKEN,
                settings.SLACK_CHANNEL,
            )

        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "success": True,
            "message": (
                "Account created! You will need to verify your email address "
                "before logging in. You may need to check your spam."
            ),
            "token": token.key,
        }, status=status.HTTP_201_CREATED)


class PasswordResetView(generics.GenericAPIView):
    """ Send a password reset email to the user given their email address. """

    serializer_class = PasswordResetSerializer

    def post(self, request):
        if not request.data['email']:
            return Response({
                "success": False,
                "message": (
                    "You must enter an email to send the password reset "
                    "request to."
                )
            }, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(email=request.data['email'])
        if user.exists():
            user = user.first()

            # send account recovery email to user
            current_site = get_current_site(request)
            send_template_email(
                user.email,
                'Password reset request for your account.',
                'acc_recover_email.html',
                {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                },
            )

        return Response({
            "success": True,
            "message": "If your email address exists in our database,"
                       " you will receive an email with instructions for"
                       " how to reset your password in a few minutes."
        }, status=status.HTTP_200_OK)


class AuthTokenSerializer(AuthTokenSerializerBase):
    def validate(self, attrs):
        username = attrs.get('username') or attrs.get('email')
        password = attrs.get('password')

        if not username or not password:
            raise serializers.ValidationError(
                'Must include "username" and "password".',
                code='authorization',
            )

        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password,
        )

        if not user:
            if User.objects.filter(email__iexact=username).exists():
                if not User.objects.get(email__iexact=username).is_active:
                    raise serializers.ValidationError(
                        (
                            'You cannot login until you have confirmed your '
                            'email address.'
                        ),
                        code='authorization',
                    )
            raise serializers.ValidationError(
                'Unable to login with provided credentials.',
                code='authorization',
            )

        attrs['user'] = user
        return attrs


class ObtainAuthToken(ObtainAuthTokenBase):
    """ Obtain an auth token used to make authorized requests to the API. """

    serializer_class = AuthTokenSerializer
    renderer_classes = (renderers.JSONRenderer, renderers.BrowsableAPIRenderer)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        if not request.session.session_key:
            request.session.cycle_key()
        return Response({
            'token': token.key,
            'sessionid': request.session.session_key,
        })


class Logout(APIView):
    """ Given an auth token, revoke the auth token and logout. """

    def get(self, request):
        if request.user.is_authenticated:
            if hasattr(request.user, "auth_token"):
                request.user.auth_token.delete()
        return Response({"success": True}, status=status.HTTP_200_OK)


class ResendConfirmationView(APIView):
    """ Resend the confirmation email to an inactive user. """

    serializer_class = PasswordResetSerializer

    def post(self, request):
        if not request.data['email']:
            return Response({
                "success": False,
                "message": (
                    "You must enter an email to send the email verification "
                    "message to."
                )
            }, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=request.data['email'])
        if user.exists() and not user.first().is_active:
            user = user.first()

            # send activation email to user
            current_site = get_current_site(request)
            send_template_email(
                user.email,
                'Activate your account!',
                'acc_active_email.html',
                {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                },
            )
        return Response({
            "success": True,
            "message": "If your email address exists in our database,"
                       " you will receive an email with instructions for"
                       " how to confirm your email address in a few minutes."
        }, status=status.HTTP_200_OK)
