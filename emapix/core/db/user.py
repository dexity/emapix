
#from emapix.core.models import *
from emapix.core.db.photo import WPhoto


class WUser(object):

    @classmethod
    def photo_request_submitter(cls, res):
        """Returns user who submitted photo for the request."""
        ph = WPhoto.request_photo(res)
        if ph is None:
            return None
        return ph.user
