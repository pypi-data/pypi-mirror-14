from __future__ import unicode_literals
from __future__ import print_function
import unittest
from ...appsensor import fpt

class FPTTest(unittest.TestCase):
    def basic_payload_test(self):
        self.assertEqual(fpt.is_file_path_traversal("foo bar"), None)

        false_params = [
          "3/.5",
          "bob.txt echo 'hi'" 
        ]

        true_params = [
          "../../../test.config", 
          "/etc/passwd"
        ]

        for param in false_params:
            print(param)
            self.assertEqual(fpt.is_file_path_traversal(param), None)

        for param in true_params:
            print(param)
            self.assertNotEqual(fpt.is_file_path_traversal(param), None)
