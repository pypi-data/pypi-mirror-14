from __future__ import unicode_literals
from __future__ import print_function
import unittest
from ...appsensor import params

class ParamsTest(unittest.TestCase):
    def sqli_params_test(self):
        test_params = {"z":"y","xyz":"aa' OR '5'= '5"}
        vuln_param = params.test_params_for_sqli(test_params)
        self.assertEqual(vuln_param["param"], "xyz")

    def xss_params_test(self):
        test_params = {"z":"y","xyz":"abc\"><script>bar"}
        vuln_param = params.test_params_for_xss(test_params)
        self.assertEqual(vuln_param["param"], "xyz")

        test_params = {"z":"y","abcd":["x","abc\"><script>bar"]}
        vuln_param = params.test_params_for_xss(test_params)
        self.assertEqual(vuln_param["param"], "abcd")