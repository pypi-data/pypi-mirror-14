#!/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2016-03-17 11:13:35
# Filename      : api.py
# Description   : 
from __future__ import print_function, unicode_literals
import requests
from dsb_requests import logs
from dsb_requests import patch_const
reload(patch_const)
import struct
import random
import time
import socket
import json

def _api_request(method, url):
    response = requests.request(method, 
            'http://{hostname}:{port}{url}'.format(
                hostname = API_HOSTNAME, port = API_PORT, url = url), 
            headers = {
                'dsb_client_key'    :       DSB_CLIENT_KEY,
                }, stream = False)

    if response.json()['status_code'] != 0:
        logs.print_error(response.json()['status_msg'] or 'error')
        return

    return response

class _UDPResponse(object):
    def __init__(self, raw_data):
        self.raw_data = raw_data

    def json():
        return json.loads(self.raw_data)

def _recvdata(conn, size):
    _buffer = ''
    while len(_buffer) < size:
        data, address = conn.recvfrom(size)
        assert address[0] == API_HOSTNAME
        _buffer += data

    return _buffer

def _udp_request(command, kw = None, conn = None):
    conn = conn or socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
    kw = kw or {}
    kw['dsb_client_key'] = DSB_CLIENT_KEY
    assert kw, 'disable send empty params'
    kw_string = json.dumps(kw)
    conn.sendto(struct.pack('!Q', len(kw_string)) + kw_string, 
            (API_HOSTNAME, int(API_PORT) + 1)) # udp接口的端口在http的情况下+ 1

    _buffer = _recvdata(conn, 4) # 前4字节表示了文本内容的长度
    buffer_length = struct.unpack('!Q', _buffer)
    return _UDPResponse(_recvdata(conn, buffer_length))

def notify_proxy_node_access_me(proxy_node, conn):
    assert not proxy_node['internet'], 'only supported node in lan'
    response = _udp_request('notify_node_penetrate', conn = conn, kw = {
        'node_ip'   :   proxy_node['ip'],
        })
    print(response.content)

    return response.json()['node_port_in_lan']

def fetch_proxy_node_response():
    """获取所有可用的节点信息"""
    try:
        response = _api_request('GET', '/api/proxy/node')
    except requests.exceptions.RequestException:
        return

    nodes = response.json()['nodes']
    return nodes

