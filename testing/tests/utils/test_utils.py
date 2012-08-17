import unittest
import time

from emapix.utils.utils import ts2h, ts2utc, ts2hd
from fixtures import *

class UtilsTest(unittest.TestCase):

    def setUp(self):
        pass
    
    
    def test_ts2hd(self):
        self.assertEqual(ts2hd(TS2), TS2_HD)
        self.assertEqual(ts2hd(TS4), TS4_HD)
        
    
    def test_ts2h(self):
        self.assertEqual(ts2h(TS, TS1, False), TS1_H)
        self.assertEqual(ts2h(TS, TS2, False), TS2_H)
        self.assertEqual(ts2h(TS, TS3, False), TS3_H)
        self.assertEqual(ts2h(TS, TS4, False), TS4_H)
        self.assertEqual(ts2h(TS, TS5, False), TS5_H)
        self.assertEqual(ts2h(TS, TS6, False), TS6_H)
        
        
    def test_ts2utc(self):
        self.assertEqual(ts2utc(TS), TS_UTC)
        