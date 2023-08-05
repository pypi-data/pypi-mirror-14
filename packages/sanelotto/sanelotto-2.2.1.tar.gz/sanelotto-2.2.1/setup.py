#!/usr/bin/env python3
#-*- coding: UTF-8 -*-

'''
@author: Vladimir37
@license MIT license
Copyright (C) 2016
'''

import os
import sys
from distutils.core import setup

if not os.access('/usr/local/bin', os.W_OK):
    raise PermissionError('Permission denied')

setup(
    name='sanelotto',
    version='2.2.1',
    author='Vladimir37',
    author_email='vladimir37work@gmail.com',
    url='http://sanelotto.info/',
    description='Automation tool for fast and simple deploy any applications to server.',
    download_url='https://github.com/Vladimir37/Sanelotto/archive/master.zip',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='setuptools deploy deployment CI Continuous Integration development',
    packages=['sanelotto']
)

link_addr = sys.path[1]
print('----------------')
print('Created symlink...')
print(link_addr + '/sanelotto/sanelotto', '/usr/local/bin/sanelotto')
print('----------------')
os.symlink(link_addr + '/sanelotto/sanelotto', '/usr/local/bin/sanelotto')
os.chmod('/usr/local/bin/sanelotto', 0o777)