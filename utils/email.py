from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from smtpapi import SMTPAPIHeader
import datetime


def send_template_email(
        to_email, subject, template, context, sent_by=None, hours=None):
    body = render_to_string(template, context)
    if hours and sent_by:
        header = SMTPAPIHeader()
        delay = datetime.timedelta(hours=hours)
        send_at = timezone.now() + delay
        header.set_send_at(int(send_at.timestamp()))
        email = EmailMultiAlternatives(
            subject,
            body,
            sent_by,
            to=[to_email],
            headers={"X-SMTPAPI": header.json_string()},
        )
    elif hours:
        header = SMTPAPIHeader()
        delay = datetime.timedelta(hours=hours)
        send_at = timezone.now() + delay
        header.set_send_at(int(send_at.timestamp()))
        email = EmailMultiAlternatives(
            subject,
            body,
            to=[to_email],
            headers={"X-SMTPAPI": header.json_string()},
        )
    elif sent_by:
        email = EmailMultiAlternatives(
            subject,
            body,
            sent_by,
            to=[to_email],
        )
    else:
        email = EmailMultiAlternatives(
            subject,
            body,
            to=[to_email],
        )

    email.attach_alternative(body, "text/html")
    email.send()
