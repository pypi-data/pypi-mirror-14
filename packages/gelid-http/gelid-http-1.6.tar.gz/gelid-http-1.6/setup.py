# -*- coding: utf-8 -*-
# Created by lvjiyong on 15/3/16
from os.path import dirname, join
from setuptools import setup, find_packages

with open(join(dirname(__file__), 'VERSION'), 'rb') as f:
    version = f.read().decode('ascii').strip()

setup(
    name="gelid-http",
    version=version,
    description=u"为python-gelid提供简单http请求服务",
    author="lvjiyong",
    url="https://github.com/lvjiyong/python-gelid",
    license="Apache2.0",
    long_description=open('README').read(),
    maintainer='lvjiyong',
    platforms=["any"],
    maintainer_email='lvjiyong@gmail.com',
    include_package_data=True,
    packages=find_packages(exclude=('tests')),
    install_requires=[
        'chardet',
    ],
)