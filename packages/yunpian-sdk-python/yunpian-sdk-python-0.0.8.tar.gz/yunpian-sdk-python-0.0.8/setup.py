# -*- coding:utf-8 -*-
#filename:setup
#16/3/30 上午10:41

__author__ = 'bingone'
from setuptools import setup, find_packages

setup(
    name = 'yunpian-sdk-python',
    version = '0.0.8',
    keywords = ('yunpian', 'sdk','python'),
    description = 'yunpian-sdk-python',
    license = 'MIT License',
    install_requires = ['requests>=2.9.1'],

    author = 'bingone',
    author_email = 'shaoyan@yunpian.com',

    packages = find_packages(),
    platforms = 'any',
)