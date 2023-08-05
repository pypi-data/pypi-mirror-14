#!/usr/bin/python
# coding=utf8

"""
    安装包工具
"""

import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

requires = [
    ]

kokolog = __import__('kokolog')
setup(name='kokolog',
version=kokolog.__version__,
description='wecatch kokolog',
author='haokuan',
author_email='jingdaohao@gmail.com',
url='https://github.com/listen-lavender/kokolog',
keywords='wecatch > ',
packages=find_packages(),
install_requires=requires,
scripts=[],
)

