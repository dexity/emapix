import os
import sys

sys.path.append('../../../')
os.environ['DJANGO_SETTINGS_MODULE'] = 'emapix.settings'

from emapix.core.models import Request, Location
from emapix.utils.google_geocoding import latlon2addr


def convert():
    locs = Location.objects.all()

    for loc in locs:
        addr = latlon2addr(loc.lat / 1e6, loc.lon / 1e6)
        print addr
        if addr is not None:
            ll = addr[0]
            loc.res_lat = ll[0] * 1e6
            loc.res_lon = ll[1] * 1e6
            (loc.street, loc.city, loc.country) = addr[1]
            loc.res_type = addr[2]
            loc.zipcode = addr[3]
            loc.save()


if __name__ == '__main__':
    convert()
