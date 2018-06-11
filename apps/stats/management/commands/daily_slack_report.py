from slacker import Slacker

from django.conf import settings
from django.core.management.base import BaseCommand

from apps.application.models import Application, Submission

MESSAGE_FORMAT = (
    ":trumpet: Daily Applications Report :trumpet: ```"
    "In-progress applications: {num_apps}\n"
    "Submitted applications: {num_submitted_apps}\n"
    "```"
)


class Command(BaseCommand):
    help = "Sends a daily statistics report to Slack."

    def handle(self, *args, **kwargs):
        num_submitted = len(set(
            Submission.objects.all().values_list("application_id", flat=True)))
        Slacker(settings.SLACK_TOKEN).chat.post_message(
            settings.SLACK_CHANNEL,
            MESSAGE_FORMAT.format(
                num_apps=Application.objects.all().count(),
                num_submitted_apps=num_submitted,
            )
        )
