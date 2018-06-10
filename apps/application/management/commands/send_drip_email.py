from datetime import timedelta

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.db.models import Count
from django.template.loader import render_to_string
from django.utils import timezone

from apps.registration.models import User


class Command(BaseCommand):
    help = "Sends a drip email to people who have registered but not applied."

    def add_arguments(self, parser):
        parser.add_argument(
            "--no-start-time",
            action="store_true",
            dest="start",
            default=False,
            help="Ignore the start range when sending emails. "
                 "Used to send emails to people who registered "
                 "before the script was installed."
        )

    def handle(self, *args, **kwargs):
        now = timezone.now()
        start_range = now - timedelta(days=settings.DRIP_EMAIL_DAYS)
        start_range = start_range.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )
        end_range = start_range + timedelta(days=1)

        if not kwargs["start"]:
            self.stdout.write(
                "Sending drip email for users registered between {} and {}..."
                .format(start_range, end_range)
            )
        else:
            self.stdout.write(
                "Sending drip email for users registered before {}..."
                .format(end_range)
            )

        users = (
            User.objects
            .annotate(num_submissions=Count("submissions"))
            .filter(num_submissions=0)
            .filter(date_joined__lt=end_range)
        )

        if not kwargs["start"]:
            users = users.filter(date_joined__gt=start_range)

        for user in users:
            message = render_to_string("drip_email.html", {
                "user": user,
                "registration_url": settings.EMAIL_REDIRECT_URL,
            })
            email = EmailMultiAlternatives(
                "Don't forget to submit your application for TotalityHacks!",
                message,
                to=[user.email],
            )
            email.attach_alternative(message, "text/html")
            email.send()

        self.stdout.write(
            "Sent drip email to {} user(s).".format(users.count())
        )
