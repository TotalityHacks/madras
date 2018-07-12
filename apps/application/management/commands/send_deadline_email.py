from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Count
from django.utils import timezone

from apps.registration.models import User

from utils.email import send_template_email


class Command(BaseCommand):
    help = "Sends a deadline email to people who have not applied."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            default=False,
            help="Don't actually send emails."
        )

    def handle(self, *args, **kwargs):
        now = timezone.now()

        users = (
            User.objects
            .annotate(num_submissions=Count("submissions"))
            .filter(num_submissions=0)
        )

        fmt_priority_deadline = settings.PRIORITY_DEADLINE.strftime("%B %d")
        fmt_final_deadline = settings.FINAL_DEADLINE.strftime("%B %d")
        passed_priority = now >= settings.PRIORITY_DEADLINE

        if passed_priority:
            template_name = 'deadline_email.html'
        else:
            template_name = 'priority_deadline_email.html'

        for user in users.distinct():
            if not kwargs["dry_run"]:
                subject = ("Don't forget to apply for TotalityHacks!")
                send_template_email(
                    user.email,
                    subject,
                    template_name,
                    {
                        "user": user,
                        "registration_url": settings.EMAIL_REDIRECT_URL,
                        "priority_deadline": fmt_priority_deadline,
                        "final_deadline": fmt_final_deadline,
                    },
                )

        self.stdout.write(
            "Sent deadline reminder email to {} user(s).".format(users.count())
        )
