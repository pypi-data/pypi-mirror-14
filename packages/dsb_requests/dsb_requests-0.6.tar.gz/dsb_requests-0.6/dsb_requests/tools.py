#!/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2016-03-17 20:00:48
# Filename      : tools.py
# Description   : 
from __future__ import print_function, unicode_literals

def is_string(s):
    return isinstance(s, (str, unicode))

def is_list_or_tuple(data):
    return isinstance(data, (tuple, list))

def to_list(data):
    return data if is_list_or_tuple(data) else [data]

