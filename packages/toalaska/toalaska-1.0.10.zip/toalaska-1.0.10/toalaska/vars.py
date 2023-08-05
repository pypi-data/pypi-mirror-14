# -*- coding: utf-8 -*-
import re


def to_lower(txt):
    return re.sub("([A-Z])","_\g<1>",txt).lower().lstrip("_")
def to_upper(txt):
    return re.sub("(_[a-z])",lambda t:t.group(1).lstrip("_").upper(),txt).lstrip("_")