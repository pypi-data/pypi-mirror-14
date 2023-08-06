# -*- coding: utf-8 -*-
# Copyright (C) 2015 tCell.io, Inc. - All Rights Reserved

""" Agent Module handles communication and instrumentation, this
is the main class.
"""

from __future__ import unicode_literals
from __future__ import print_function

import threading
from queue import Queue, Empty, Full
import os
import json

from .common import *
from tcell_agent.instrumentation import safe_wrap_function

from tcell_agent.agent import TCellAgent, PolicyTypes
import logging
import tcell_agent.tcell_logger
LOGGER = logging.getLogger('tcell_agent').getChild(__name__)

appsensorLock = threading.Lock()

class AppSensorManager(object):
    def __init__(self):
        self._appsensor_thread = None
        self._appsensor_thread_pid = os.getpid()
        self._appsensor_queue = Queue(100)
        self.use_threads = True

    def ensure_appsensor_thread_running(self):
        if self.is_appsensor_thread_running():
            return
        appsensorLock.acquire()
        try:
            if self.is_appsensor_thread_running():
                return
            self.start_appsensor_thread()
        finally:
            appsensorLock.release()

    def is_appsensor_thread_running(self):
        return self._appsensor_thread and self._appsensor_thread.isAlive() and self._appsensor_thread_pid == os.getpid()

    def start_appsensor_thread(self):
        """Start the background threads for polling/events"""
        def run_appsensor_thread():
            while True:
                metadata = self._appsensor_queue.get(True)
                try:
                    if metadata:
                        if metadata.do_request:
                            self.run_appsensor_for_request(metadata)
                        if metadata.do_response:
                            self.run_appsensor_for_response(metadata)
                except Exception as e:
                    LOGGER.debug("Exception running appsensor")
                    LOGGER.debug(e)
        self._appsensor_thread = threading.Thread(target=run_appsensor_thread, args=())
        self._appsensor_thread.daemon = True # Daemonize thread
        self._appsensor_thread.start()
        self._appsensor_thread_pid = os.getpid()

    def run_appsensor_for_request(self, appsensor_meta):
        if appsensor_meta is None:
            return
        appsensor_policy = TCellAgent.get_policy(PolicyTypes.APPSENSOR)
        if appsensor_policy is None:
            return
        json_body = None
        if (appsensor_meta.json_body_str is not None):
            try:
                if isinstance(appsensor_meta.json_body_str, bytes):
                    json_body = json.loads(appsensor_meta.json_body_str.decode("utf-8"))
                else:
                    json_body = json.loads(appsensor_meta.json_body_str)
            except Exception as e:
                LOGGER.debug("Error decoding json")
                LOGGER.debug(e)
        if appsensor_policy.get_option("req_res_size"):
            safe_wrap_function("Check Request Size", request_size, appsensor_meta, appsensor_meta.request_content_len)
        if appsensor_policy.get_option("xss"):
            safe_wrap_function("Checking GET vars xss", test_for_xss, "get", appsensor_meta, appsensor_meta.get_dict)
            safe_wrap_function("Checking POST vars xss", test_for_xss, "post", appsensor_meta, appsensor_meta.post_dict)
            safe_wrap_function("Checking JSON vars xss", test_for_xss, "json", appsensor_meta, json_body)
            safe_wrap_function("Checking Cookies vars xss", test_for_xss, "cookies", appsensor_meta, appsensor_meta.cookie_dict)
        if appsensor_policy.get_option("sqli"):
            safe_wrap_function("Checking GET vars sqli", test_for_sqli, "get", appsensor_meta, appsensor_meta.get_dict)
            safe_wrap_function("Checking POST vars sqli", test_for_sqli, "post", appsensor_meta, appsensor_meta.post_dict)
            safe_wrap_function("Checking JSON vars sqli", test_for_sqli, "json", appsensor_meta, json_body)
            safe_wrap_function("Checking Cookies vars sqli", test_for_sqli, "cookies", appsensor_meta, appsensor_meta.cookie_dict)
        if appsensor_policy.get_option("cmdi"):
            safe_wrap_function("Checking GET vars cmdi", test_for_cmdi, "get", appsensor_meta, appsensor_meta.get_dict)
            safe_wrap_function("Checking POST vars cmdi", test_for_cmdi, "post", appsensor_meta, appsensor_meta.post_dict)
            safe_wrap_function("Checking JSON vars cmdi", test_for_cmdi, "json", appsensor_meta, json_body)
        if appsensor_policy.get_option("fpt"):
            safe_wrap_function("Checking GET vars fpt", test_for_fpt, "get", appsensor_meta, appsensor_meta.get_dict)
            safe_wrap_function("Checking POST vars fpt", test_for_fpt, "post", appsensor_meta, appsensor_meta.post_dict)
            safe_wrap_function("Checking JSON vars fpt", test_for_fpt, "json", appsensor_meta, json_body)
        if appsensor_policy.get_option("null"):
            safe_wrap_function("Checking GET vars null", test_for_null, "get", appsensor_meta, appsensor_meta.get_dict)
            safe_wrap_function("Checking POST vars null", test_for_null, "post", appsensor_meta, appsensor_meta.post_dict)
            safe_wrap_function("Checking JSON vars null", test_for_null, "json", appsensor_meta, json_body)
        if appsensor_policy.get_option("retr"):
            safe_wrap_function("Checking GET vars retr", test_for_return, "get", appsensor_meta, appsensor_meta.get_dict) 

    def run_appsensor_for_response(self, appsensor_meta):
        if appsensor_meta is None:
            return
        appsensor_policy = TCellAgent.get_policy(PolicyTypes.APPSENSOR)
        if appsensor_policy.get_option("req_res_size"):
            safe_wrap_function("Check response size", response_size, appsensor_meta, appsensor_meta.response_content_len)
        if appsensor_policy.get_option("resp_codes"):
            safe_wrap_function("Check response code", response_code, appsensor_meta, appsensor_meta.response_code)

    def send_appsensor_data(self, appsensor_meta_data):
        """Add an event to the queue to be sent to tcell"""
        if appsensor_meta_data is None:
            return
        if self.use_threads == False:
            self.run_appsensor_for_request(appsensor_meta_data)
        else:
            self.ensure_appsensor_thread_running()
            try:
                self._appsensor_queue.put_nowait(appsensor_meta_data)
            except Full:
                LOGGER.debug("Appsensor queue full")

app_sensor_manager = AppSensorManager()

