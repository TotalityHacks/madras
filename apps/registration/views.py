import datetime

from django.http import JsonResponse
from django.contrib.auth import login
from django.urls import reverse
from django.conf import settings

from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from .tokens import account_activation_token
from .models import User

from smtpapi import SMTPAPIHeader


@api_view(['GET'])
def index(request):
    """The API for Madras, a cloud-based hackathon management system."""
    return Response({
        '/registration': 'Endpoints relating to user account creation.',
        '/reader': 'Endpoints relating to reading applications.',
        '/login': 'Obtain a token for authenticated requests.',
        '/logout': 'Revoke the current session and logout of the API.',
        '/stats': (
            'Get statistics about currently submitted and reviewed '
            'applications.'
        ),
        '/application': 'Endpoints relating to submitting applications.',
        '/checkin': (
            'Endpoints related to attendee checkin on the day of the event.'),
    })


@api_view(['GET'])
def home(request):
    """ Show information about registration endpoints. """
    return Response({
        reverse('registration:home'): (
            'Get information about registration endpoints.'),
        reverse('registration:signup'): 'Create a new account.',
        reverse('registration:reset'): (
            'Send a password reset given an email account.'),
        reverse('registration:resend_email'): (
            'Resend a confirmation email to an unverified user.'),
    })


def activate(request, uidb64, token):
    """
    Handles the link the user uses to confirm their account.
    Should not be called directly through the API.
    """
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        # schedule intro email to be sent
        header = SMTPAPIHeader()
        send_at = timezone.now() + datetime.timedelta(hours=settings.INTRO_EMAIL_DELAY)
        header.set_send_at(int(send_at.timestamp()))
        message = render_to_string('intro_email.txt')
        mail_subject = 'Thanks for applying!'
        email = EmailMultiAlternatives(
            mail_subject,
            message,
            "John Reinstra <john@totalityhacks.com>",
            to=[user.email],
            headers={"X-SMTPAPI": header.json_string()}
        )
        email.attach_alternative(message, "text/html")
        email.send()

        # activate user
        user.is_active = True
        user.email_confirmed = True
        user.save()
        login(request, user)
        return redirect(settings.EMAIL_REDIRECT_URL)
    else:
        return redirect(settings.EMAIL_REDIRECT_FAILURE_URL)


def recover(request, uidb64, token):
    """
    Handles a password recover request.
    Should not be called directly through the API.
    """
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is None or not account_activation_token.check_token(user, token):
        return JsonResponse(
            {"success": False, "error": "Invalid password reset code!"})

    context = {
        "email": user.email,
        "action": request.path_info
    }

    if request.method == "POST":
        password = request.POST.get("password")
        if password and len(password) >= 8:
            user.set_password(password)
            user.save()
            return redirect(settings.EMAIL_REDIRECT_URL)
        else:
            context["error"] = "Password is too short!"

    return render(request, "reset_password.html", context)
