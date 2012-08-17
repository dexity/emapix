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

def time_list(ts):
    "Converts timestamp to list: [day, hour, minute]"
    d   = ts / (60*60*24)
    h   = ts / (60*60) - d*24
    m   = ts / 60 - h*60 - d*24*60
    return [d, h, m]
    
    

def ts2hd(ts, show_year=True):
    "Converts timestamp to date string"
    df   = "%b %d, %H:%M"
    if show_year:
        df  = "%b %d, %Y %H:%M"
    return time.strftime(df, time.gmtime(int(ts)))


def show_year(ts0, ts1):
    "Returns true when years for ts0 and ts1 are different"
    y0  = time.gmtime(int(ts0)).tm_year
    y1  = time.gmtime(int(ts1)).tm_year
    return y0 != y1
    

def ts2h(ts0, ts1=None, full=True):
    "Converts timestamp to human readible string"
    if ts1 is None:
        return ts2hd(ts0)
    dt  = int(ts1) - int(ts0)
    if (dt < 0):    # Invalid time
        return ""
    sy  = show_year(ts0, ts1)
    if (dt > 432000):    # More than 5 days
        return ts2hd(ts0, sy)
    ht  = ""
    tl  = time_list(dt)
    # Compose string
    if tl[0] != 0:
        ht  = "%s d %s hr" % (tl[0], tl[1])
    elif tl[1] != 0:
        ht  = "%s hr %s min" % (tl[1], tl[2])
    elif tl[2] != 0:
        ht  = "%s min" % tl[2]
    else:
        ht  = "1 min"
    if full:
        ht  += " ago"
    return ht


def ts2utc(ts):
    "Gets timestamp and returns string in format: YYYY-MM-DD hh:mm:ssZ"
    try:
        utc = time.strftime("%Y-%m-%d %H:%M:%SZ", time.gmtime(float(ts)))
    except Exception, e:    # Common exceptions: TypeError
        utc = ""
    return utc
