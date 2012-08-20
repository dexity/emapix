import unittest

from emapix.utils.google_geocoding import latlon2addr
from fixtures import *

class GeocodingTest(unittest.TestCase):

    def setUp(self):
        pass
    
    
    @unittest.skip("Makes request to service")
    def test_latlon2addr(self):
        res = latlon2addr(*LATLON0)
        self.assertEqual(res, None)
        
        res = latlon2addr(*LATLON1)
        self.assertEqual(res, ADDR1)
        
        res = latlon2addr(*LATLON2)
        self.assertEqual(res, ADDR2)
        
        res = latlon2addr(*LATLON3)
        self.assertEqual(res, ADDR3)
        
        res = latlon2addr(*LATLON4)
        self.assertEqual(res, ADDR4)
    
    