#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: xiaohuihui
# Created Time:  2016-4-12 
#############################################


from setuptools import setup, find_packages

setup(
    name = "myfirstpip",
    version = "0.0.6",
    keywords = ("pip"),
    description = "my first pip",
    long_description = "my first pip",
    license = "MIT Licence",

    url = "http://xiaohhhh.github.io/",
    author = "xiaohhhh",
    author_email = "xiaohhhh@gmail.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = []
)