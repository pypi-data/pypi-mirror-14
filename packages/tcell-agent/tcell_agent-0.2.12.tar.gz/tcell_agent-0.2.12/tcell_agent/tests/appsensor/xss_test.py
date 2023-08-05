from __future__ import unicode_literals
from __future__ import print_function
import unittest
from ...appsensor import xss

class XSSTest(unittest.TestCase):
    def basic_payload_test(self):
        self.assertEqual(xss.is_xss("foo bar"), None)
        self.assertNotEqual(xss.is_xss("foo<script>alert(1)</script>"), None)

        false_params = [
          "abc def", 
          "O'Reilly",
          "this script is false. <h1> hi"
        ]

        true_params = [
          "abc\"><script>", 
          "<script>",
          "O'><img src='x' onerror='alert(1)'>Reilly",
          "O'><img/src='x' onerror='alert(1)'>Reilly",
          "\"><script>alert(/XSSPOSED/);</script>"
        ]

        for param in false_params:
            print(param)
            self.assertEqual(xss.is_xss(param), None)

        for param in true_params:
            print(param)
            self.assertNotEqual(xss.is_xss(param), None)
