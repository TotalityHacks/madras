from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db.models import Count
from django.utils import timezone
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from apps.registration.models import User


class Command(BaseCommand):
    help = "Sends a drip email to people who have registered but not applied."

    def handle(self, *args, **kwargs):
        now = timezone.now()
        time_threshold = now - timedelta(days=settings.DRIP_EMAIL_DAYS)
        users = User.objects.annotate(num_submissions=Count("submissions")) \
                            .filter(num_submissions=True) \
                            .filter(date_joined__lt=time_threshold) \
                            .filter(sent_drip_email=False)
        num_users = users.count()

        for user in users:
            message = render_to_string("drip_email.html", {
                "user": user,
                "registration_url": settings.EMAIL_REDIRECT_DRIP_URL
            })
            email = EmailMultiAlternatives(
                "Don't forget to register for TotalityHacks!",
                message,
                to=[user.email]
            )
            email.attach_alternative(message, "text/html")
            email.send()

            user.sent_drip_email = True
            user.save(update_fields=["sent_drip_email"])

        self.stdout.write("Sent drip email to {} user(s).".format(num_users))
