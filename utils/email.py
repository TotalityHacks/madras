from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from smtpapi import SMTPAPIHeader
import datetime

def send_template_email(to_array, subject, template, context, sent_by=None):
    body = render_to_string(template, context)
    if sent_by != None:
        email = EmailMultiAlternatives(
            mail_subject,
            message,
            sent_by,
            to=to_array
        )
    else:
        email = EmailMultiAlternatives(
            mail_subject,
            message,
            to=to_array
        )       

    email.attach_alternative(message, "text/html")
    email.send()

def send_delayed_email(to_array, subject, template, context, hours, sent_by=None):
    # hours = hours until send (self-explanatory)
    header = SMTPAPIHeader().set_send_at(timezone.now() + datetime.timedelta(hours=hours))
    body = render_to_string(template, context)
    if sent_by != None:
        email = EmailMultiAlternatives(
            mail_subject,
            message,
            sent_by,
            to=to_array,
            headers={"X-SMTPAPI": header.json_string()}
        )
    else:
        email = EmailMultiAlternatives(
            mail_subject,
            message,
            to=to_array,
            headers={"X-SMTPAPI": header.json_string()}
        )

    email.attach_alternative(message, "text/html")
    email.send()        


