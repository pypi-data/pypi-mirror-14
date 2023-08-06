# -*- coding: utf-8 -*-
# Copyright (C) 2015 tCell.io, Inc. - All Rights Reserved

from .xss import is_xss
from .sqli import is_sqli
from .cmdi import is_cmdi
from .fpt import is_file_path_traversal
from .misc_sensors import has_null, has_return

import time
import sys

def test_param(param_name, param_value, test_func):
  if param_name is None or param_value is None:
    return None
  if isinstance(param_value, dict):
    for new_param_name in param_value:
      result = test_param(new_param_name, param_value[new_param_name], test_func)
      if result:
        return result
  elif isinstance(param_value, list):
    for new_param_value in param_value:
      result = test_param(param_name, new_param_value, test_func)
      if result:
        return result
  else:
    if isinstance(param_value, bytes):
      param_value = param_value.decode('utf-8')
    param_type = str(type(param_value))

    if(param_type == "<class 'str'>" or param_type == "<type 'str'>" or param_type == "<type 'unicode'>"):
      try:
        param_value = str(param_value)
        match = test_func(param_value)
        if match is not None:
            return {"m":match, "param":param_name, "value":param_value}
      except:
        pass
  return None

def test_params(params, test_func):
    if params is None:
      return
    return test_param("request", params, test_func)

def test_params_for_sqli(params):
    return test_params(params, is_sqli)

def test_params_for_xss(params):
    return test_params(params, is_xss)

def test_params_for_cmdi(params):
    return test_params(params, is_cmdi)

def test_params_for_fpt(params):
    return test_params(params, is_file_path_traversal)

def test_params_for_null(params):
    return test_params(params, has_null)

def test_params_for_return(params):
    return test_params(params, has_return)