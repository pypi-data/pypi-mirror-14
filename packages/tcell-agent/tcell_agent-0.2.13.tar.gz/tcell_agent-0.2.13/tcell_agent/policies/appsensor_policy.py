# -*- coding: utf-8 -*-
# Copyright (C) 2015 tCell.io, Inc. - All Rights Reserved

from tcell_agent.policies import TCellPolicy

class AppSensorPolicy(TCellPolicy):
    api_identifier = "appsensor"
    options = [
        "req_res_size",
        "resp_codes",
        "xss",
        "sqli",
        "cmdi",
        "fpt",
        "null",
        "retr",
        "login_failure"]

    def __init__(self, policy_json=None):
        super(AppSensorPolicy, self).__init__()
        self.init_variables()
        if policy_json is not None:
            self.loadFromJson(policy_json)

    def init_variables(self):
        self.enabled = False
        self.options = {}

    def get_option(self, option):
        return self.options.get(option, False)

    def loadFromJson(self, policy_json):
        if "policy_id" in policy_json:
            self.policy_id = policy_json["policy_id"]
        else:
            raise Exception("Policy Id Not Found")
        self.init_variables()
        policy_data = policy_json.get("data")
        if policy_data:
            options_json = policy_data.get("options")
            if options_json:
                for option in AppSensorPolicy.options:
                    self.options[option] = options_json.get(option, False)
        pass