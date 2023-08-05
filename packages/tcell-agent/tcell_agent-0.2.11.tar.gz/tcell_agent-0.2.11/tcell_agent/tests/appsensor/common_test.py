from __future__ import unicode_literals
from __future__ import print_function
import unittest
from ...appsensor import common
import re

class CommmonTest(unittest.TestCase):
    def create_payload_none_test(self):
        payload = common.create_payload(None,None)
        self.assertEqual(payload, None)

    def create_payload_test(self):
        test = re.match(".*","ABCDEFGHIJKLMNOP")
        payload = common.create_payload(test,"ABCDEFGHIJKLMNOP ABCDEFGHIJKLMNOP ABCDEFGHIJKLMNOP ABCDEFGHIJKLMNOP ABCDEFGHIJKLMNOP ABCDEFGHIJKLMNOP ABCDEFGHIJKLMNOP ABCDEFGHIJKLMNOP ABCDEFGHIJKLMNOP ABCDEFGHIJKLMNOP ABCDEFGHIJKLMNOP ABCDEFGHIJKLMNOP")
        self.assertEqual(payload, "ABCDEFGHIJKLMNOP ABCDEFGHIJKLMNOP ABCDEFGHIJKLMNOP ABCDEFGHIJKLMNOP ABCDEFGHIJKLMNOP ABCDEFGHIJKLMNOP ABCDEFGHIJKLMNOP ABCDEFGHIJKLMNOP ABCDEFGHIJKLMNOP ABCDEFGHIJKLMNOP ABCDEFGHIJKLMNOP ABCDEFGHIJKLMNOP")

    def create_payload_test_small(self):
        test = re.match(".*","ABCDEFGHIJKLMNOP")
        payload = common.create_payload(test,"ABCDEFGHIJKLMNOP")
        self.assertEqual(payload, "ABCDEFGHIJKLMNOP")
