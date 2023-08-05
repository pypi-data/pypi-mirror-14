# -*- coding: utf-8 -*-
# Copyright (C) 2015 tCell.io, Inc. - All Rights Reserved

from __future__ import unicode_literals
from __future__ import print_function

from ..sensor_events import AppSensorEvent
from ..sanitize import SanitizeUtils
from .meta import AppSensorMeta
from .params import test_params_for_xss
from .params import test_params_for_sqli
from .params import test_params_for_cmdi
from .params import test_params_for_fpt,test_params_for_null,test_params_for_return
import re
from ..agent import TCellAgent
import json
from ..config import CONFIGURATION

MAX_NORMAL_REQUEST_BYTES = 1024*512
MAX_NORMAL_RESPONSE_BYTES = 1024*1024*2

# Detection Points
DP_XSS = "xss"
DP_SQLI = "sqli"
DP_CMDI = "cmdi"
DP_FILE_PATH_TRAVERSAL = "fpt"
DP_NULL = "null"
DP_RETURN = "retr"

DP_LOGIN_FAILURE = "lgnFlr"
DP_LOGIN_SUCCESS = "lgnSccss"

DP_UNUSUAL_REQUEST_SIZE = "reqsz"
DP_UNUSUAL_RESPONSE_SIZE = "rspsz"
DP_RESPONSE_401 = "s401"
DP_RESPONSE_403 = "s403"
DP_RESPONSE_404 = "s404"
DP_RESPONSE_4xx = "s4xx"
DP_RESPONSE_500 = "s500"
DP_RESPONSE_5xx = "s5xx"

RESPONSE_CODE_DP_DICT = {
    401:DP_RESPONSE_401,
    403:DP_RESPONSE_403,
    404:DP_RESPONSE_404,
    4:DP_RESPONSE_4xx, 
    500:DP_RESPONSE_500,
    5:DP_RESPONSE_5xx
}

SRE_MATCH_TYPE = type(re.match("",""))

def sendEvent(
    meta,
    detection_point,
    parameter,
    data,
    payload=None):
    TCellAgent.send(AppSensorEvent(
        detection_point,
        parameter,
        meta.location,
        meta.remote_address,
        meta.route_id,
        data,
        meta.method,
        payload=payload,
        user_id=meta.user_id,
        hmacd_session_id=meta.session_id,
    ))

def login_failed(app_sensor_meta, username):
    if username is not None:
        username = SanitizeUtils.hmac(username)
    sendEvent(
        app_sensor_meta, 
        DP_LOGIN_FAILURE, 
        username,
        payload=None)

def request_size(app_sensor_meta, str_length):
    if (str_length > MAX_NORMAL_REQUEST_BYTES):
        sendEvent(
          app_sensor_meta, 
          DP_UNUSUAL_REQUEST_SIZE, 
          str(str_length),
          None)

def response_size(app_sensor_meta, str_length):
    if (str_length > MAX_NORMAL_RESPONSE_BYTES):
        sendEvent(
          app_sensor_meta, 
          DP_UNUSUAL_RESPONSE_SIZE, 
          str(str_length),
          None)

def response_code(app_sensor_meta, response_code):
    if response_code == 200:
        return
    dp = RESPONSE_CODE_DP_DICT.get(response_code)
    if dp is None:
        code_series = int(response_code / 100)
        dp = RESPONSE_CODE_DP_DICT.get(code_series)
    if dp:
        sendEvent(
          app_sensor_meta, 
          dp, 
          str(response_code),
          None)

def create_payload(match, param_value):
    if match is None or param_value is None:
        return None
    if (isinstance(match, SRE_MATCH_TYPE) == False):
        return None
    return param_value

def handle_injection(app_sensor_meta, dp, type_of_param, vuln_results):
    if vuln_results:
        vuln_param = vuln_results.get("param")
        payload=None
        if vuln_param:
            if CONFIGURATION.allow_unencrypted_appsensor_payloads:
                if vuln_param.lower() in CONFIGURATION.blacklisted_params:
                    payload = "BLACKLISTED"

                elif CONFIGURATION.whitelist_present and not(vuln_param.lower() in CONFIGURATION.whitelisted_params):
                     payload = "NOT_WHITELISTED"

                else:
                    payload = create_payload(vuln_results.get("m"), vuln_results.get("value"))

            sendEvent(
                app_sensor_meta,
                dp,
                vuln_param,
                json.dumps({"t":type_of_param}),
                payload)

def test_for_xss(area, app_sensor_meta, param_dict):
    handle_injection(app_sensor_meta, DP_XSS, area, test_params_for_xss(param_dict))

def test_for_sqli(area, app_sensor_meta, param_dict):
    handle_injection(app_sensor_meta, DP_SQLI, area, test_params_for_sqli(param_dict))

def test_for_cmdi(area, app_sensor_meta, param_dict):
    handle_injection(app_sensor_meta, DP_CMDI, area, test_params_for_cmdi(param_dict))

def test_for_fpt(area, app_sensor_meta, param_dict):
    handle_injection(app_sensor_meta, DP_FILE_PATH_TRAVERSAL, area, test_params_for_fpt(param_dict))

def test_for_null(area, app_sensor_meta, param_dict):
    handle_injection(app_sensor_meta, DP_NULL, area, test_params_for_null(param_dict))

def test_for_return(area, app_sensor_meta, param_dict):
    handle_injection(app_sensor_meta, DP_RETURN, area, test_params_for_return(param_dict))

