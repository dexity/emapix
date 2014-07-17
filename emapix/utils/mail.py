
from django.core import mail as django_mail
from google.appengine.api import mail as gae_mail
from django.conf import settings

def send_mail(subject, message, from_email, recipient_list, fail_silently=False):
    if settings.DEBUG:
        print subject, message, from_email, recipient_list
        django_mail.send_mail(subject, message, from_email, recipient_list, fail_silently=fail_silently)
    else:
        gae_mail.send_mail(sender=from_email, to=recipient_list, subject=subject, body=message)
