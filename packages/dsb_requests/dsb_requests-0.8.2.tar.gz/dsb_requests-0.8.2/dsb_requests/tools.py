#!/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2016-03-17 20:00:48
# Filename      : tools.py
# Description   : 
from __future__ import print_function, unicode_literals
import socket

def is_string(s):
    return isinstance(s, (str, unicode))

def is_list_or_tuple(data):
    return isinstance(data, (tuple, list))

def to_list(data):
    return data if is_list_or_tuple(data) else [data]

def made_conn():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return s

