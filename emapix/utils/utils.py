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


def ts2hd(ts):
    "Converts time stamp to date string"
    return time.strftime("%b %d, %Y %H:%M", time.gmtime(float(ts)))


def ts2h(ts0, ts1=None, full=True):
    "Converts time stamp to human readible string"
    if ts1 is None:
        return ts2hd(ts0)
    dt  = float(ts1) - float(ts0)


def ts2utc(ts):
    "Gets timestamp and returns string in format: YYYY-MM-DD hh:mm:ssZ"
    try:
        utc = time.strftime("%Y-%m-%d %H:%M:%SZ", time.gmtime(float(ts)))
    except Exception, e:    # Common exceptions: TypeError
        utc = ""
    return utc
