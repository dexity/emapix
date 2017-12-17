import os
import sys

sys.path.append('../../../')
os.environ['DJANGO_SETTINGS_MODULE'] = 'emapix.settings'

from emapix.core.models import Request, Location


def migrate():
    reqs = Request.objects.all()
    for req in reqs:
        l = Location()
        l.lat = req.lat
        l.lon = req.lon
        l.save()
        req.location = l
        req.save()


if __name__ == '__main__':
    migrate()
