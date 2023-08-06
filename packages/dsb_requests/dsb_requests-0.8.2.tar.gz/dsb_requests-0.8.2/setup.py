#!/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2016-03-17 17:57:21
# Filename      : setup.py
# Description   : 
from setuptools import setup

_special_module = []
try:
    import optparse
except ImportError:
    _special_module.append('optparse')

setup(
        name = 'dsb_requests',
        version = '0.8.2',
        author = 'tuxpy',
        include_package_data = True,
        packages = [
            'dsb_requests',
            ],
        install_requires = ['requests', 'lxml', 'mock'] + _special_module,
        description = 'duoshoubang \'s requests',
        scripts = ['bin/dsb_requests'],
        )

