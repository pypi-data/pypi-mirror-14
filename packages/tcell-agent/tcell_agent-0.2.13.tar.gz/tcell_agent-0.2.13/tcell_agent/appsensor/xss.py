# -*- coding: utf-8 -*-
# Copyright (C) 2015 tCell.io, Inc. - All Rights Reserved

import re

SAFE_PATTERN = re.compile("^[a-zA-Z0-9_\s\r\n\t]*$")

PATTERNS = [
    r"(?:<(script|iframe|embed|frame|frameset|object|img|applet|body|html|style|layer|link|ilayer|meta|bgsound))",
    r"(?:(alert|on\w+|function\s+\w+)\s*\(\s*(['+\d\w](,?\s*['+\d\w]*)*)*\s*\))",
    r"(?:\"[^\"]*[^-]?>)|(?:[^\w\s]\s*\/>)|(?:>\")",
    r"(?:\"+.*[<=]\s*\"[^\"]+\")|(?:\"\s*\w+\s*=)|(?:>\w=\/)|(?:#.+\)[\"\s]*>)|(?:\"\s*(?:src|style|on\w+)\s*=\s*\")|(?:[^\"]?\"[,;\s]+\w*[\[\(])"
    r"(?:^>[\w\s]*<\/?\w{2,}>)",
    r"(?:with\s*\(\s*.+\s*\)\s*\w+\s*\()|(?:(?:do|while|for)\s*\([^)]*\)\s*\{)|(?:\/[\w\s]*\[\W*\w)",
    r"(?:[=(].+\?.+:)|(?:with\([^)]*\)\))|(?:\.\s*source\W)",
    r"(?:[\".]script\s*\()|(?:\$\$?\s*\(\s*[\w\"])|(?:\/[\w\s]+\/\.)|(?:=\s*\/\w+\/\s*\.)|(?:(?:this|window|top|parent|frames|self|content)\[\s*[(,\"]*\s*[\w\$])|(?:,\s*new\s+\w+\s*[,;)])",
    r"(?:=\s*\w+\s*\+\s*\")|(?:\+=\s*\(\s\")|(?:!+\s*[\d.,]+\w?\d*\s*\?)|(?:=\s*\[s*\])|(?:\"\s*\+\s*\")|(?:[^\s]\[\s*\d+\s*\]\s*[;+])|(?:\"\s*[&|]+\s*\")|(?:\/\s*\?\s*\")|(?:\/\s*\)\s*\[)|(?:\d\?.+:\d)|(?:\]\s*\[\W*\w)|(?:[^\s]\s*=\s*\/)",
    r"<iframe.*"
]

COMPILED_PATTERNS = [re.compile(pattern, flags=re.IGNORECASE|re.S|re.M) for pattern in PATTERNS]

def is_xss(param_value):
    if SAFE_PATTERN.search(param_value):
        return None
    for pattern in COMPILED_PATTERNS:
        pattern_result = pattern.search(param_value)
        if(pattern_result):
            return pattern_result
    return None
