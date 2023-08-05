#!/usr/bin/env python
#coding:utf-8
"""
  Author:  fly --<yafeile@sohu.com>
  Purpose: 
  Created: Monday, March 14, 2016
"""

import base64

def parser(url):
    """解析QQ旋风下载地址"""
    try:
        url = base64.b64decode(url)
        return url
    except TypeError:
        return 'The Given URL is unvalid'

if __name__ == '__main__':
    unittest.main()