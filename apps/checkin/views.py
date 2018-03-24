from django.http import JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from madras import settings

def gen_qr_code(request):
    print(request.GET["email"])