# -*- coding: utf-8 -*-
# Copyright (C) 2015 tCell.io, Inc. - All Rights Reserved

import re

SAFE_PATTERN = re.compile("^[a-zA-Z0-9_\s\r\n\t]*$")

CMDI_PATTERNS = [
    r"(?:[\;\|\`]\W*?\bcc|\b(wget|curl))\b|\/cc(?:[\'\"\|\;\`\-\s]|$)",
    r"(?:\b(?:(?:n(?:et(?:\b\W+?\blocalgroup|\.exe)|(?:map|c)\.exe)|t(?:racer(?:oute|t)|elnet\.exe|clsh8?|ftp)|(?:w(?:guest|sh)|rcmd|ftp)\.exe|echo\b\W*?\by+)\b|c(?:md(?:(?:\.exe|32)\b|\b\W*?\\\/c)|d(?:\b\W*?[\\\/]|\W*?\.\.)|hmod.{0,40}?\+.{0,3}x))|[\;\|\`]\W*?\b(?:(?:c(?:h(?:grp|mod|own|sh)|md|pp)|p(?:asswd|ython|erl|ing|s)|n(?:asm|map|c)|f(?:inger|tp)|(?:kil|mai)l|(?:xte)?rm|ls(?:of)?|telnet|uname|echo|id)\b|g(?:\+\+|cc\b)))"
]

COMPILED_PATTERNS = [re.compile(pattern, flags=re.IGNORECASE|re.S|re.M) for pattern in CMDI_PATTERNS]

def is_cmdi(param_value):
    if SAFE_PATTERN.search(param_value):
        return None
    for pattern in COMPILED_PATTERNS:
        pattern_result = pattern.search(param_value)
        if(pattern_result):
            return pattern_result
    return None