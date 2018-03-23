from django.http import JsonResponse
from django.contrib.auth import login
from .forms import SignupForm, ApplicationForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.shortcuts import render
from .tokens import account_activation_token
from .models import Applicant
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt

OVERRIDE_SENDING_EMAIL = True

def home(request):
    if request.method == 'POST':
        form = ApplicationForm(data=request.POST, instance=request.user.application)
        form.save()
        return JsonResponse({"success": True})
    elif request.method == 'GET':
        form = [ApplicationForm(instance=request.user.application) if request.user.is_authenticated else None]
        return render(request, 'home.html', {
            'user': request.user,
            'form': form,
            'domain': get_current_site(request).domain,
        })

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        form = SignupForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = OVERRIDE_SENDING_EMAIL
            user.save()
            if OVERRIDE_SENDING_EMAIL:
                return JsonResponse({"success": True})
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
            return JsonResponse({"success": False, "err_field": form.errors})
    if request.method == "GET":
        return render(request, 'signup.html', {
            'form': SignupForm(),
            'user': request.user,
            'domain': get_current_site(request).domain,
        })


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
        return JsonResponse({"error": "Invalid email confirmation!"})
