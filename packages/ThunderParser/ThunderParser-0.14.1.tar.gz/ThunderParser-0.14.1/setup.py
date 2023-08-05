# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 23:36:20 2015

@author: fly
"""


import os
from setuptools import setup, find_packages


def read_file(filename):
    filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                            filename)
    if os.path.exists(filepath):
        return open(filepath).read()
    else:
        return ''

setup(name='ThunderParser',
      version='0.14.1',
      platforms = ['Posix', 'Mac OS', 'Windows'], 
      description='Parse the software of thunder,qqdl and flashget download url',
      long_description=read_file('README.rst'),
      author='fly',
      author_email='yafeile@sohu.com',
      url='https://github.com/yafeile/ThunderParser',
      classifiers=[
                  'License :: OSI Approved :: BSD License',
                  'Programming Language :: Python',
      ],
      packages=find_packages(),
      keywords=['download', 'parser'],
      license='BSD License'
      )
