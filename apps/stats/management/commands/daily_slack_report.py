import datetime

from utils.slack import send_to_slack

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.application.models import Application, Submission

SLACK_MESSAGE_FORMAT = (
    ":trumpet: Daily Applications Report :trumpet: ```"
    "In-progress applications: {num_apps}\n"
    "Submitted applications: {num_submitted_apps}\n"
    "In-progress applications (last 24 hrs): {num_apps_24hrs}\n"
    "Submitted applications (last 24 hrs): {num_submitted_apps_24hrs}\n"
    "```"
)
SLACK_REPORT_CHANNELS = [
    settings.SLACK_CHANNEL,
    "#outreach",
]


class Command(BaseCommand):
    help = "Sends a daily statistics report to Slack."

    def handle(self, *args, **kwargs):
        last24hrs = timezone.now() - datetime.timedelta(days=1)
        num_apps_24hrs = (Application.objects
                          .filter(created_at__gt=last24hrs).count())
        num_submitted = len(set(
            Submission.objects.all().values_list("application_id", flat=True)
        ))
        num_submitted_24hrs = len(set(
            Submission.objects
            .filter(created_at__gt=last24hrs)
            .values_list("application_id", flat=True)
        ))
        for slack_channel in SLACK_REPORT_CHANNELS:
            send_to_slack(
                SLACK_MESSAGE_FORMAT.format(
                    num_apps=Application.objects.all().count(),
                    num_submitted_apps=num_submitted,
                    num_apps_24hrs=num_apps_24hrs,
                    num_submitted_apps_24hrs=num_submitted_24hrs,
                ),
                settings.SLACK_TOKEN,
                slack_channel,
                )
