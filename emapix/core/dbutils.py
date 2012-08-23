

def remove_request(res):
    "Removes request. Can through exception"
    req     = Request.objects.get(resource=res)
    req.location.delete()   # Remove location
    req.delete()
    return True
    