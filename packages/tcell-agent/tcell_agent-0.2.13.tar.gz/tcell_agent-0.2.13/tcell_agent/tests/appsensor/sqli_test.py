from __future__ import unicode_literals
from __future__ import print_function
import unittest
from ...appsensor.sqli import is_sqli

class XSSTest(unittest.TestCase):
    def basic_payload_test(self):
        self.assertEqual(is_sqli("foo bar"), None)
        self.assertNotEqual(is_sqli("fooa\" OR \"5\"= \"5"), None)

    def full_payload_test(self):

        false_params = [
          "abc def", 
          "O'Reilly",
          "555--",
          "555--666",
          "I should order by friday",
          "b<img src=\"a\"><script>alert(1)</script>"
        ]

        true_params = [
          "a\" OR \"5\"= \"5", 
          "a' OR '5'= '5",
          "a';--",
          "a'--",
          "10 OrDeR By 10--"
        ]

        for param in false_params:
            print(param)
            self.assertEqual(is_sqli(param), None)

        for param in true_params:
            print(param)
            self.assertNotEqual(is_sqli(param), None)
