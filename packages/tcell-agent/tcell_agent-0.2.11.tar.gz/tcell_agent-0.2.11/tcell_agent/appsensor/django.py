# -*- coding: utf-8 -*-
# Copyright (C) 2015 tCell.io, Inc. - All Rights Reserved

from __future__ import unicode_literals
from __future__ import print_function

from .common import *
from tcell_agent.instrumentation import safe_wrap_function
from tcell_agent.instrumentation.django.routes import get_route_table

from tcell_agent.agent import TCellAgent, PolicyTypes


def django_meta(request):
  meta = AppSensorMeta(
      request._tcell_context.remote_addr ,
      request.META.get("REQUEST_METHOD"),
      request.get_full_path(),
      request._tcell_context.route_id,
      session_id=request._tcell_context.session_id,
      user_id=request._tcell_context.user_id
  )
  return meta

def appsensor_login_failed(request, username):
    appsensor_policy = TCellAgent.get_policy(PolicyTypes.APPSENSOR)
    if appsensor_policy is None:
        return
    if appsensor_policy.get_option("login_failure"):
        meta = django_meta(request)
        login_failed(meta, username)

def django_request_appsensor(request):
    pass

def django_response_appsensor(django_response, request, response):
    meta = django_meta(request)
    appsensor_policy = TCellAgent.get_policy(PolicyTypes.APPSENSOR)
    if appsensor_policy is None:
        return
    if appsensor_policy.get_option("req_res_size"):
        request_len = 0
        try:
          request_len = int(request.META.get("CONTENT_LENGTH",0))
        except:
          pass
        safe_wrap_function("Check Request Size", request_size, meta, request_len)
        if isinstance(response, django_response):
            safe_wrap_function("Check response size", response_size, meta, len(response.content))
    if appsensor_policy.get_option("xss"):
        safe_wrap_function("Checking GET vars", test_for_xss, "get", meta, request.GET)
        safe_wrap_function("Checking POST vars", test_for_xss, "post", meta, request.POST)
        safe_wrap_function("Checking Cookies vars", test_for_xss, "cookies", meta, request.COOKIES)
    if appsensor_policy.get_option("sqli"):
        safe_wrap_function("Checking GET vars sqli", test_for_sqli, "get", meta, request.GET)
        safe_wrap_function("Checking POST vars sqli", test_for_sqli, "post", meta, request.POST)
        safe_wrap_function("Checking Cookies vars sqli", test_for_sqli, "cookies", meta, request.COOKIES)
    if appsensor_policy.get_option("cmdi"):
        safe_wrap_function("Checking GET vars cmdi", test_for_cmdi, "get", meta, request.GET)
        safe_wrap_function("Checking POST vars cmdi", test_for_cmdi, "post", meta, request.POST)
    if appsensor_policy.get_option("fpt"):
        safe_wrap_function("Checking GET vars fpt", test_for_fpt, "get", meta, request.GET)
        safe_wrap_function("Checking POST vars fpt", test_for_fpt, "post", meta, request.POST)
    if appsensor_policy.get_option("null"):
        safe_wrap_function("Checking GET vars fpt", test_for_null, "get", meta, request.GET)
        safe_wrap_function("Checking POST vars fpt", test_for_null, "post", meta, request.POST)
    if appsensor_policy.get_option("retr"):
        safe_wrap_function("Checking GET vars retr", test_for_return, "get", meta, request.GET)
    if appsensor_policy.get_option("resp_codes"):
        safe_wrap_function("Check response code", response_code, meta, response.status_code)
