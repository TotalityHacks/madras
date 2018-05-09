from django.http import JsonResponse
from django.contrib.auth import login
from django.urls import reverse
from django.conf import settings

from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.shortcuts import redirect, render

from .tokens import account_activation_token
from .models import User

from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode


@api_view(['GET'])
def index(request):
    """ The backend API for Madras, a cloud-based hackathon management system. """
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
        reverse('registration:reset'): 'Send a password reset given an email account.'
    })


def activate(request, uidb64, token):
    """ Handles the link the user uses to confirm their account. Should not be called directly through the API. """
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect(settings.EMAIL_REDIRECT_URL)
    else:
        return JsonResponse({"success": False, "error": "Invalid email confirmation!"})


def recover(request, uidb64, token):
    """ Handles a password recover request. Should not be called directly through the API. """
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is None or not account_activation_token.check_token(user, token):
        return JsonResponse({"success": False, "error": "Invalid password reset code!"})
    if request.method == "POST":
        password = request.POST.get("password")
        if password:
            user.set_password(password)
            user.save()
        return redirect(settings.EMAIL_REDIRECT_URL)
    else:
        return render(request, "reset_password.html", {"action": request.path_info})
