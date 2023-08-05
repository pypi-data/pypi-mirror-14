# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 23:23:24 2015

@author: fly
"""
import base64

def _parser(url):
    """解析迅雷下载链接"""
    try:
        url = base64.b64decode(url)
        url = url[2:-2]
        return url
    except TypeError:
        return 'The Given URL is unvalid'

def parser(url):
    """兼容0.14.1之前版本的下载链接"""
    protocol, url = url.split("://")
    length = len(url)
    d, c = divmod(length, 4)
    if c > 0:
        url = url + (4 - c) * '='
    protocol = protocol.lower()
    if protocol == 'thunder':
        _parser(url)