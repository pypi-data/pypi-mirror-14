#!/usr/bin/env python
# -*- coding: utf-8 -*-
def md5(txt):
    import hashlib
    m = hashlib.md5()
    m.update(txt)
    return m.hexdigest()