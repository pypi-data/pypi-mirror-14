# -*- coding: utf-8 -*-
# Copyright (C) 2015 tCell.io, Inc. - All Rights Reserved

from .xss import is_xss
from .sqli import is_sqli
from .cmdi import is_cmdi
from .fpt import is_file_path_traversal
from .misc_sensors import has_null, has_return

def test_params(params, test_func):
    for param_name in params:
        if isinstance(params[param_name], list): 
          for param_value in params[param_name]:
              match = test_func(param_value)
              if match is not None:
                  return {"m":match, "param":param_name, "value":param_value}
        else:
          match = test_func(params[param_name])
          if match is not None:
              return {"m":match, "param":param_name, "value":params[param_name]}
    return None

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