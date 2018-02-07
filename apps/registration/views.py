from django.http import JsonResponse
from django.contrib.auth import login
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from .models import Applicant
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt


def home(request):
    pass


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        form = SignupForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate your account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "err_field": form.errors, "req": request.POST})


def activate(request, uidb64, token):
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
        return JsonResponse({"message": "invalid email confirmation"})
