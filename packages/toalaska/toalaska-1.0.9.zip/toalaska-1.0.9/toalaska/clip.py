#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
windows 下的剪贴板操作类
'''
import win32clipboard as w
import win32con
from PIL import ImageGrab

def get_text():
    w.OpenClipboard()
    d = w.GetClipboardData(win32con.CF_TEXT)
    w.CloseClipboard()
    return d
def set_text(aString):
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(win32con.CF_TEXT, aString)
    w.CloseClipboard()

def get_img():
    im = ImageGrab.grabclipboard()
    return im