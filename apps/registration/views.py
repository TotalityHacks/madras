from django.http import JsonResponse
from django.contrib.auth import login
from django.urls import reverse

from rest_framework.response import Response
from rest_framework.decorators import api_view

from .tokens import account_activation_token
from .models import Applicant

from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode


@api_view(['GET'])
def home(request):
    """ Show information about registration endpoints. """
    return Response({
        reverse('registration:home'): 'Get information about registration endpoints.',
        reverse('registration:signup'): 'Create a new account.',
        reverse('registration:activate'): 'Handler to validate user email confirmations. Should not be called directly.'
    })


def activate(request, uidb64, token):
    """ Handles the link the user uses to confirm their account. Should not be called directly. """
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Applicant.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Applicant.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return JsonResponse({"message": 'Thank you for your email confirmation. Now you can login your account.'})
    else:
        return JsonResponse({"error": "Invalid email confirmation!"})
