from django.contrib.auth import context_processors as cp
from django.contrib.auth.models import AnonymousUser

from emapix.core.models import UserProfile
import logging


def auth(request):
    """Custom authentication context processor."""
    aparams = cp.auth(request)
    user = aparams['user']
    if isinstance(user, AnonymousUser):
        userprof = ''    # Empty UserProfile?
    else:
        try:
            userprof = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            logging.error('User profile does not exist')
            userprof = ''

    aparams['userprof'] = userprof  # Update dictionary
    return aparams
