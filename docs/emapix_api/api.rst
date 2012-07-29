.. _api:

Web Service API
===============

http://www.emapix.com/v1/api

Required params:
    key         - api key
    location    - pair of latitude and longitude separated by comma: latitude,longitude
    radius      - distance (in meters) within which to return results

Example request:

http://www.emapix.com/v1/api?location=-33.8670522,151.1957362
    
Example response:
{
    "status":   "ok",
    "result":   {}
}    


