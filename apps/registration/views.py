from django.http import JsonResponse
from django.contrib.auth import login
from django.urls import reverse
from django.conf import settings

from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.shortcuts import redirect

from .tokens import account_activation_token
from .models import User

from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode


@api_view(['GET'])
def index(request):
    return Response({
        '/registration': 'Endpoints relating to user account creation.',
        '/reader': 'Endpoints relating to reading applications.',
        '/login': 'Obtain a token for authenticated requests.',
        '/logout': 'Revoke the current session and logout of the API.',
        '/stats': 'Get statistics about currently submitted and reviewed applications.',
        '/application': 'Endpoints relating to submitting applications.'
    })


@api_view(['GET'])
def home(request):
    """ Show information about registration endpoints. """
    return Response({
        reverse('registration:home'): 'Get information about registration endpoints.',
        reverse('registration:signup'): 'Create a new account.',
    })


def activate(request, uidb64, token):
    """ Handles the link the user uses to confirm their account. Should not be called directly. """
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect(settings.HOME_PAGE_URL)
    else:
        return JsonResponse({"error": "Invalid email confirmation!"})
