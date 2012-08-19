"""
Useful utils for Google Geocoding API:
    https://developers.google.com/maps/documentation/geocoding
"""

import urllib2
import json

URL_BASE    = "http://maps.googleapis.com/maps/api/geocode/json"

def latlon2addr(lat, lon):
    """
    Reverse geocoding: converts (lat, lon) to address tuple of tuples.
    Examples:
    1. Valid response
            (32.816547, -117.261629) =>
            ((32.8165539, -117.261437), ("1064 Skylark Dr", "La Jolla, CA", "United States"), "ROOFTOP")
    2. Invalid response (something happened)
            (32.816547, -117.261629) => None
    3. Incomplete address
            (32.616577, -117.70824) =>
            ((37.09024, -95.712891), (None, None, "United States"), "APPROXIMATE")
    4. Response with no lat or lon (hardly possible)
            ((None, None), (None, None, "United States"), "APPROXIMATE")
    """
    url = "%s?latlng=%s,%s&sensor=false" % (URL_BASE, lat, lon)
    (street, city, country) = (None, None, None)    # Default
    try:
        req = urllib2.Request(url)
        res = urllib2.urlopen(req)
        s   = res.read()
        js  = json.loads(s)        
    except Exception, e:
        return (None, None, None)

    status  = js["status"]
    if status == "OK" and len(js["results"]) > 0:
        adr_comp    = js["results"][0]["address_components"]    # Most specific
        for comp in adr_comp:
            if "street_number" in comp["types"]:
                street  = comp["long_name"] + " "
            elif "route" in comp["types"]:
                if street is None:
                    street = ""
                street  += comp["long_name"]
            elif "sublocality" in comp["types"]:
                city    = comp["long_name"]
            elif "locality" in comp["types"] and city is None:
                city    = comp["long_name"] # If "sublocality" is empty
            elif "administrative_area_level_2" in comp["types"] and city is None:
                city    = comp["long_name"] # If "sublocality" or "locality" are empty
            elif "administrative_area_level_1" in comp["types"]:    # state
                if city is None:
                    city = ""
                else:
                    city += ", "
                city    += comp["short_name"]
            elif "country" in comp["types"]:
                country = comp["long_name"]
            
    #    print json.dumps(adr_comp, indent=4)
    #
    ## Dumping
    #latlon  = js["results"][0]["geometry"]["location"]
    #address = "%s, %s, %s" % (street, city, country)
    #print "(%s, %s) | %s | (%s, %s)" % (lat, lon, address, latlon["lat"], latlon["lng"])    
    
    return (street, city, country)