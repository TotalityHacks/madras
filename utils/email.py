from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from smtpapi import SMTPAPIHeader
import datetime

def send_template_email(to_array, subject, template, context, sent_by=None):
    body = render_to_string(template, context)
    if sent_by != None:
        email = EmailMultiAlternatives(
            subject,
            body,
            sent_by,
            to=to_array
        )
    else:
        email = EmailMultiAlternatives(
            subject,
            body,
            to=to_array
        )       

    email.attach_alternative(body, "text/html")
    email.send()

def send_delayed_email(to_array, subject, template, context, hours, sent_by=None):
    # hours = hours until send (self-explanatory)
    header = SMTPAPIHeader()
    delay = datetime.timedelta(hours=settings.INTRO_EMAIL_DELAY)
    send_at = timezone.now() + delay
    header.set_send_at(int(send_at.timestamp()))
    body = render_to_string(template, context)
    if sent_by != None:
        email = EmailMultiAlternatives(
            subject,
            body,
            sent_by,
            to=to_array,
            headers={"X-SMTPAPI": header.json_string()}
        )
    else:
        email = EmailMultiAlternatives(
            subject,
            body,
            to=to_array,
            headers={"X-SMTPAPI": header.json_string()}
        )

    email.attach_alternative(body, "text/html")
    email.send()        


