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
from urllib.parse import quote_plus
import qrcode
import os.path

static_path = "static/checkin/qr_codes/"


def get_qr_code(request):
    try:
        applicant = Applicant.objects.get(email=request.GET["email"])
    except Applicant.DoesNotExist:
        return JsonResponse({"success": False, "err_field": "User does not exist."})
    # TODO: check that applicant was actually admitted
    return JsonResponse({"success": True, "qr_image_path": "/" + return_qr(applicant.email)})


def get_qr_codes(request):
    # TODO: will need to be authenticated to admins
    applicants = Applicant.objects.all()
    # TODO: filter to only include admitted applicants
    files = []
    for applicant in applicants:
        files.append(return_qr(applicant.email))
    return JsonResponse({"success": True, "qr_image_paths": files})


def return_qr(email):
    safe_email = email.replace("@", "").replace(".", "") + ".png"
    relative_path = static_path + safe_email
    full_path = os.path.join(settings.PROJECT_ROOT, relative_path)
    if not os.path.exists(full_path):
        with open(full_path, "wb") as f:
            qrcode.make(safe_email).save(f, format="PNG")
    return relative_path
