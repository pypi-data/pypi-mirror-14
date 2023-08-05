# -*- coding: utf-8 -*-
# Copyright (C) 2015 tCell.io, Inc. - All Rights Reserved

import re

SAFE_PATTERN = re.compile("^[a-zA-Z0-9_\s\r\n\t]*$")

PATH_TRAVERSAL_REGEXES = [
    r"(?:(?:\/|\\)?\.+(\/|\\)(?:\.+)?)|(?:\w+\.exe\??\s)|(?:;\s*\w+\s*\/[\w*-]+\/)|(?:\d\.\dx\|)|(?:%(?:c0\.|af\.|5c\.))|(?:\/(?:%2e){2})",
    r"(?:%c0%ae\/)|(?:(?:\/|\\)(home|conf|usr|etc|proc|opt|s?bin|local|dev|tmp|kern|[br]oot|sys|system|windows|winnt|program|%[a-z_-]{3,}%)(?:\/|\\))|(?:(?:\/|\\)inetpub|localstart\.asp|boot\.ini)",
    r"(?:etc\/\W*passwd)"
]

COMPILED_PATTERNS = [re.compile(pattern, flags=re.IGNORECASE|re.S|re.M) for pattern in PATH_TRAVERSAL_REGEXES]

def is_file_path_traversal(param_value):
    if SAFE_PATTERN.search(param_value):
        return None
    for pattern in COMPILED_PATTERNS:
        pattern_result = pattern.search(param_value)
        if(pattern_result):
            return pattern_result
    return None