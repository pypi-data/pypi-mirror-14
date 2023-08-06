# -*- coding: utf-8 -*-
# Copyright (C) 2015 tCell.io, Inc. - All Rights Reserved

import re

SAFE_PATTERN = re.compile("^[a-zA-Z0-9_\s\r\n\t]*$")

NULL_REGEX = re.compile(r"\0", flags=re.IGNORECASE|re.S|re.M)
RETURN_REGEX = re.compile(r"(\n|\r)", flags=re.IGNORECASE|re.S|re.M)

def has_null(param_value):
    pattern_result =  NULL_REGEX.search(param_value)
    if pattern_result:
        return pattern_result
    return None

def has_return(param_value):
    pattern_result =  RETURN_REGEX.search(param_value)
    if pattern_result:
        return pattern_result
    return None
