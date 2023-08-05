#!/usr/bin/env python
# -*- coding: utf-8 -*-

SCREENSHOT_METHOD_UIAUTOMATOR = 'uiautomator'
SCREENSHOT_METHOD_MINICAP = 'minicap'
SCREENSHOT_METHOD_AUTO = 'auto'

IMAGE_MATCH_METHOD_TMPL = 'template'
IMAGE_MATCH_METHOD_SIFT = 'sift'

EVENT_UIAUTO_TOUCH = 1 <<0
EVENT_UIAUTO_CLICK = 1 <<0 # alias for touch
EVENT_UIAUTO_SWIPE = 2 <<0
