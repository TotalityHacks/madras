from django.http import JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from madras import settings
from apps.registration.models import Applicant

def gen_qr_code(request):
    try:
        applicant = Applicant.objects.get(email=request.GET["email"])
    except Applicant.DoesNotExist:
        return JsonResponse({"success": False, "err_field": "User does not exist."})
    # TODO: check that applicant was actually admitted

