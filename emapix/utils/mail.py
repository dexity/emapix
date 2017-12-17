
from google.appengine.api import mail as gae_mail
from django.conf import settings
import sendgrid


def send_mail(subject, message, from_email, recipient_list):
    if settings.DEBUG:
        # User SendGrid client
        sg = sendgrid.SendGridClient(
            settings.SENDGRID_USERNAME, settings.SENDGRID_PASSWORD)
        m = sendgrid.Mail(to=recipient_list, subject=subject,
                          text=message, from_email=from_email)
        return sg.send(m)  # status, msg
    else:
        gae_mail.send_mail(sender=from_email, to=recipient_list,
                           subject=subject, body=message)
