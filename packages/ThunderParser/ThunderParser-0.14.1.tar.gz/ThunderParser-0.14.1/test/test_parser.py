#!/usr/bin/env python
#coding:utf-8
"""
  Author:  yafeile --<yafeile@163.com>
  Purpose: 
  Created: Monday, March 14, 2016
"""

import unittest
import os
import sys

basedir = os.path.abspath(os.path.dirname(__name__))
basedir = os.path.dirname(basedir)

sys.path.append(basedir)
from ThunderParser import parser

class Parser(unittest.TestCase):
    def test_thunder(self):
        url = 'thunder://QUFmdHA6Ly9nOmdAZHguZGwxMjM0LmNvbTo4O' \
              'DA4LyVFOCVCNSVBNCVFOSU4MSU5M0JEJUU1JTlCJUJEJUU3J' \
              'UIyJUE0JUU1JThGJThDJUU4JUFGJUFEJUU0JUI4JUFEJUU1J' \
              'UFEJTk3WyVFNyU5NCVCNSVFNSVCRCVCMSVFNSVBNCVBOSVFNS' \
              'VBMCU4Mnd3dy5keTIwMTguY29tXS5ta3ZaWg=='
        result = parser(url)
        origin ="""ftp://g:g@dx.dl1234.com:8808/%E8%B5%A4%E9%81%93BD%E5%9B%BD%E7%B2%A4%E5%8F%8C%E8%AF%AD%E4%B8%AD%E5%AD%97[%E7%94%B5%E5%BD%B1%E5%A4%A9%E5%A0%82www.dy2018.com].mkv"""
        self.assertEqual(result, origin)
    
    def test_qqdl(self):
        url = "qqdl://aHR0cDovL3Rvb2wubHUvdGVzdC56aXA="
        origin = "http://tool.lu/test.zip"
        result = parser(url)
        self.assertEqual(result, origin)
    
    def test_flashget(self):
        url = "flashget://W0ZMQVNIR0VUXWh0dHA6Ly90b29sLmx1L3Rlc3QuemlwW0ZMQVNIR0VUXQ=="
        origin = "http://tool.lu/test.zip"
        result = parser(url)
        self.assertEqual(result, origin)
    
    def test_notImplement_protocol(self):
        url = "ftp://some-url-for-test"
        self.assertRaises(NotImplementedError)
        
    def test_fix_url(self):
        url = "flashget://W0ZMQVNIR0VUXWh0dHA6Ly90b29sLmx1L3Rlc3QuemlwW0ZMQVNIR0VUXQ"
        self.assertRaises(TypeError, parser(url))
        

if __name__ == '__main__':
    unittest.main()