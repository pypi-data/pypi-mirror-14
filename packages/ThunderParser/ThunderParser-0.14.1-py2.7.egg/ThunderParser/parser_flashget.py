#!/usr/bin/env python
#coding:utf-8
"""
  Author:  fly --<yafeile@sohu.com>
  Purpose: 
  Created: Monday, March 14, 2016
"""

import base64

def parser(url):
    """解析快车下载地址"""
    try:
        url = base64.b64decode(url)
        url = url[10:-10]
        return url
    except:
        return 'The Given URL is unvalid'