from emapix.core.models import *

class WComment(object):
    
    @classmethod
    def add_comment(cls, user, req, text):
        "Adds comment"
        com = Comment(user=user, text=text)
        com.save()
        
        reqcom  = RequestComment(request=req, comment=com)
        reqcom.save()
        
        return com