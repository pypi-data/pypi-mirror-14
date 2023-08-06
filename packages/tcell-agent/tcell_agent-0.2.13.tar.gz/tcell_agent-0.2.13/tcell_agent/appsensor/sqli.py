# -*- coding: utf-8 -*-
# Copyright (C) 2015 tCell.io, Inc. - All Rights Reserved

import re

SAFE_PATTERN = re.compile("^[a-zA-Z0-9_\s\r\n\t]*$")

PATTERNS = [
  r"(?:(?:\d[\"'`´’‘]\s+[\"'`´’‘]\s+\d)|(?:^admin\s*?[\"'`´’‘]|(\/\*)+[\"'`´’‘]+\s?(?:--|#|\/\*|{)?)|(?:[\"'`´’‘]\s*?\b(x?or|div|like|between|and)\b\s*?[+<>=(),-]\s*?[\d\"'`´’‘])|(?:[\"'`´’‘]\s*?[^\w\s]?=\s*?[\"'`´’‘])|(?:[\"'`´’‘]\W*?[+=]+\W*?[\"'`´’‘])|(?:[\"'`´’‘]\s*?[!=|][\d\s!=+-]+.*?[\"'`´’‘(].*?$)|(?:[\"'`´’‘]\s*?[!=|][\d\s!=]+.*?\d+$)|(?:[\"'`´’‘]\s*?like\W+[\w\"'`´’‘(])|(?:\sis\s*?0\W)|(?:where\s[\s\w\.,-]+\s=)|(?:[\"'`´’‘][<>~]+[\"'`´’‘]))",
  r"\b(?:having)\b\s+(\d{1,10}|'[^=]{1,10}')\s*?[=<>]|(?:\bexecute(\s{1,5}[\w\.$]{1,5}\s{0,3})?\()|\bhaving\b ?(?:\d{1,10}|[\'\"][^=]{1,10}[\'\"]) ?[=<>]+|(?:\bcreate\s+?table.{0,20}?\()|(?:\blike\W*?char\W*?\()|(?:(?:(select(.*?)case|from(.*?)limit|order\sby)))|exists\s(\sselect|select\Sif(null)?\s\(|select\Stop|select\Sconcat|system\s\(|\b(?:having)\b\s+(\d{1,10})|'[^=]{1,10}')",
  r"([';]--|--[\s\r\n\v\f]|(?:--[^-]*?-)|([^\-&])#.*?[\s\r\n\v\f]|;?\\x00)",
  r"(?:(?:@.+=\s*?\(\s*?select)|(?:\d+\s*?(x?or|div|like|between|and)\s*?\d+\s*?[\-+])|(?:\/\w+;?\s+(?:having|and|x?or|div|like|between|and|select)\W)|(?:\d\s+group\s+by.+\()|(?:(?:;|#|--)\s*?(?:drop|alter))|(?:(?:;|#|--)\s*?(?:update|insert)\s*?\w{2,})|(?:[^\w]SET\s*?@\w+)|(?:(?:n?and|x?x?or|div|like|between|and|not |\|\||\&\&)[\s(]+\w+[\s)]*?[!=+]+[\s\d]*?[\"'`´’‘=()]))",
  r"(?:(?:in\s*?\(+\s*?select)|(?:(?:n?and|x?x?or|div|like|between|and|not |\|\||\&\&)\s+[\s\w+]+(?:regexp\s*?\(|sounds\s+like\s*?[\"'`´’‘]|[=\d]+x))|([\"'`´’‘]\s*?\d\s*?(?:--|#))|(?:[\"'`´’‘][\%&<>^=]+\d\s*?(=|x?or|div|like|between|and))|(?:[\"'`´’‘]\W+[\w+-]+\s*?=\s*?\d\W+[\"'`´’‘])|(?:[\"'`´’‘]\s*?is\s*?\d.+[\"'`´’‘]?\w)|(?:[\"'`´’‘]\|?[\w-]{3,}[^\w\s.,]+[\"'`´’‘])|(?:[\"'`´’‘]\s*?is\s*?[\d.]+\s*?\W.*?[\"'`´’‘]))",
  #r"(?:(?:[\"'`´’‘]\s*?\*.+(?:x?or|div|like|between|and|id)\W*?[\"'`´’‘]\d)|(?:\^[\"'`´’‘])|(?:^[\w\s\"'`´’‘-]+(?<=and\s)(?<=or|xor|div|like|between|and\s)(?<=xor\s)(?<=nand\s)(?<=not\s)(?<=\|\|)(?<=\&\&)\w+\()|(?:[\"'`´’‘][\s\d]*?[^\w\s]+\W*?\d\W*?.*?[\"'`´’‘\d])|(?:[\"'`´’‘]\s*?[^\w\s?]+\s*?[^\w\s]+\s*?[\"'`´’‘])|(?:[\"'`´’‘]\s*?[^\w\s]+\s*?[\W\d].*?(?:#|--))|(?:[\"'`´’‘].*?\*\s*?\d)|(?:[\"'`´’‘]\s*?(x?or|div|like|between|and)\s[^\d]+[\w-]+.*?\d)|(?:[()\*<>%+-][\w-]+[^\w\s]+[\"'`´’‘][^,]))",
  r"(?:(?:\d[\"'`´’‘]\s+[\"'`´’‘]\s+\d)|(?:^admin\s*?[\"'`´’‘]|(\/\*)+[\"'`´’‘]+\s?(?:--|#|\/\*|{)?)|(?:[\"'`´’‘]\s*?\b(x?or|div|like|between|and)\b\s*?[+<>=(),-]\s*?[\d\"'`´’‘])|(?:[\"'`´’‘]\s*?[^\w\s]?=\s*?[\"'`´’‘])|(?:[\"'`´’‘]\W*?[+=]+\W*?[\"'`´’‘])|(?:[\"'`´’‘]\s*?[!=|][\d\s!=+-]+.*?[\"'`´’‘(].*?$)|(?:[\"'`´’‘]\s*?[!=|][\d\s!=]+.*?\d+$)|(?:[\"'`´’‘]\s*?like\W+[\w\"'`´’‘(])|(?:\sis\s*?0\W)|(?:where\s[\s\w\.,-]+\s=)|(?:[\"'`´’‘][<>~]+[\"'`´’‘]))"
]

COMPILED_PATTERNS = [re.compile(pattern, flags=re.IGNORECASE|re.S|re.M) for pattern in PATTERNS]

def is_sqli(param_value):
    if SAFE_PATTERN.search(param_value):
        return None
    for pattern in COMPILED_PATTERNS:
        pattern_result = pattern.search(param_value)
        if(pattern_result):
            return pattern_result
    return None

