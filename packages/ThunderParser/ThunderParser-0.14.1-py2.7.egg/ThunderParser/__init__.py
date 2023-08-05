#!/usr/bin/env python
#coding:utf-8
"""
  Author:  fly --<yafeile@sohu.com>
  Purpose: 
  Created: Monday, March 14, 2016
"""

def parser(url):
    """解析迅雷或QQ旋风下载链接"""
    protocol, url = url.split("://")
    length = len(url)
    d, c = divmod(length, 4)
    if c > 0:
        url = url + (4 - c) * '='
    protocol = protocol.lower()
    if protocol == 'thunder':
        import parser_thunder as thunder
        return thunder._parser(url)
    elif protocol == 'qqdl':
        import parser_qqdl as qqdl
        return qqdl.parser(url)
    elif protocol == 'flashget':
        import parser_flashget as flashget
        return flashget.parser(url)
    else:
        return NotImplemented