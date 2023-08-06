# coding=utf-8
'''
Created on Mar 30, 2016

@author: yangjie
'''
from setuptools import (setup, find_packages)
setup(
    name="wizard_interface",
    version="1.0.5",
    description="interface test, python, open sourced",
    author="Jie Yang",
    author_email="chnyangjie@gmail.com",
    url="http://wizard.ren",
    license="MIT",
    packages=find_packages(),
    extras_require={
        "dicttoxml": "dicttoxml",
        "xmltodict": "xmltodict",
        "beautifulsoup4": "beautifulsoup4",
        "pymysql": "pymysql",
    },
)
