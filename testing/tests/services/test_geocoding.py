import unittest
from emapix.utils.google_geocoding import latlon2addr

class GeocodingTest(unittest.TestCase):

    def setUp(self):
        pass
    
    
    def test_latlon2addr(self):
        res = latlon2add(LATLON0)
        print res
    
    