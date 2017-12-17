from emapix.utils.mail import send_mail

from emapix.settings import NOREPLY_EMAIL


ACTIV_URL = 'http://%s/confirm/%s'
ACTIV_MESSAGE = """
Hi, %s!

Please confirm your registration by following the link: %s

Explore the world!
Emapix Team

P.S. If you received this email by error, please ignore it.

"""

FORGOT_URL = 'http://%s/password/renew/%s'
FORGOT_MESSAGE = """
Hi, %s!

You have requested the password renewal. To renew your password please follow the link: %s 

Explore the world!
Emapix Team

P.S. If you received this email by error, please ignore it.

"""

NEWPASS_MESSAGE = """
Hi, %s!

The new password has been applied to your account.

Explore the world!
Emapix Team

P.S. If you received this email by error, please ignore it.

"""


def send_activation_email(request, email, username, token):
    """Send verification email."""
    url = ACTIV_URL % (request.META['SERVER_NAME'], token)
    msg = ACTIV_MESSAGE % (username, url)

    send_mail('Verify registration', msg, NOREPLY_EMAIL, [email, ])


def send_forgot_email(request, email, username, token):
    """Send forgot email."""
    url = FORGOT_URL % (request.META['SERVER_NAME'], token)
    msg = FORGOT_MESSAGE % (username, url)

    send_mail('Renew password', msg, NOREPLY_EMAIL, [email, ])


def send_newpass_confirm_email(request, email, username):
    """Sends confirmation that new password has been set."""
    msg = NEWPASS_MESSAGE % username

    send_mail('New password', msg, NOREPLY_EMAIL, [email, ])
