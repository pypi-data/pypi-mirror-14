from __future__ import unicode_literals
from __future__ import print_function

import unittest
from ...policies.appsensor_policy import AppSensorPolicy
import json

policy_one = """
{
    "policy_id":"abc-abc-abc",
    "data": {
        "options": {
            "xss":true
        }
    }
}
"""

class AppSensorPolicyTest(unittest.TestCase):
    def classname_test(self):
        self.assertEqual(AppSensorPolicy.api_identifier, "appsensor")

    def read_appensor_policy_test(self):
        policy_json = json.loads(policy_one)
        policy = AppSensorPolicy()
        self.assertEqual(policy.get_option("xss"), False)
        policy.loadFromJson(policy_json)
        self.assertEqual(policy.get_option("xss"), True)

