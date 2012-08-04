import hashlib
import time

def sha1(value):
    "Returns hex digest value of sha1 encryption"
    m   = hashlib.sha1()
    m.update(value)
    return m.hexdigest()


def random16():
    # Returns 16 characters string
    return sha1(str(time.time()))[:16]


def timestamp():
    return int(time.time())



    
