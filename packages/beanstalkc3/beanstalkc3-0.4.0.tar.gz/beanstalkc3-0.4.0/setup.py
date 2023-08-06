#!/usr/bin/env python
import os
from setuptools import setup

from beanstalkc import __version__ as src_version

PKG_VERSION = os.environ.get('BEANSTALKC_PKG_VERSION', src_version)

setup(
    name='beanstalkc3',
    version=PKG_VERSION,
    py_modules=['beanstalkc'],

    author='Dennis Kaarsemaker & Andreas Bolka',
    author_email='dennis@kaarsemaker.net',
    description='A simple beanstalkd client library (python 3 compatible fork)',
    long_description='''
beanstalkc is a simple beanstalkd client library for Python. `beanstalkd
<http://kr.github.com/beanstalkd/>`_ is a fast, distributed, in-memory
workqueue service.

After waiting for more than a year for python3-compatibility fixes to end up in
a release, it's time to fork this apparently unmaintained library.
''',
    url='http://github.com/seveas/beanstalkc',
    license='Apache License, Version 2.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
