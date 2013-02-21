from emapix.core.models import *

from emapix.utils.logger import Logger
logger = Logger.get("emapix.core.db")

class WComment(object):
    
    @classmethod
    def add_comment(cls, user, req, text):
        "Adds comment"
        com = Comment(user=user, text=text)
        com.save()
        
        reqcom  = RequestComment(request=req, comment=com)
        reqcom.save()
        
        return com
    
    
    @classmethod
    def remove_comments(cls, res):
        "Removes all request comments"
        try:
            reqcoms = RequestComment.objects.filter(request__resource=res)
            for rq in reqcoms:  # Need more efficient?
                rq.comment.delete()
            reqcoms.delete()
            return True
        except Exception, e:
            return False
