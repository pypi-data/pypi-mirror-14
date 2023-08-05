from __future__ import unicode_literals
from __future__ import print_function
import unittest
from ...appsensor import cmdi

class CMDITest(unittest.TestCase):
    def basic_payload_test(self):
        self.assertEqual(cmdi.is_cmdi("foo bar"), None)

        false_params = [
          "bob.txt echo 'hi'", 
        ]

        true_params = [
          "bob.txt; echo 'hi'", 
        ]

        for param in false_params:
            print(param)
            self.assertEqual(cmdi.is_cmdi(param), None)

        for param in true_params:
            print(param)
            self.assertNotEqual(cmdi.is_cmdi(param), None)
