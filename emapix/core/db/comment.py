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
    
    
    @classmethod
    def remove_comments(cls, res):
        "Removes all request comments"
        reqcoms = RequestComment.objects.filter(request__resource=res)
        cls.remove_req_comments(reqcoms)
    
    
    @classmethod
    def remove_comment(cls, com_id):
        "Removes request comment"
        reqcoms = RequestComment.objects.filter(comment__id = com_id)
        cls.remove_req_comments(reqcoms)   


    @classmethod
    def remove_req_comments(cls, reqcoms):
        "Removes request comments"
        for rq in reqcoms:  # Need more efficient?
            rq.comment.delete()
            rq.delete()
        