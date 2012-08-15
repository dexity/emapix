import unittest
import time

from emapix.utils.utils import ts2h, ts2utc
from fixtures import *

class UtilsTest(unittest.TestCase):

    def setUp(self):
        pass
    
    
    def test_ts2h(self):
        
        print "Hello world!"
        
        
    def test_ts2utc(self):
        self.assertEqual(ts2utc(TS), TS_UTC)
        