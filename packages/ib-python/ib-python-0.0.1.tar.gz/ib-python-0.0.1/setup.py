#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""IbPy - Interactive Brokers Python API

IbPy is a third-party implementation of the API used for accessing the
Interactive Brokers on-line trading system.  IbPy implements functionality
that the Python programmer can use to connect to IB, request stock ticker
data, submit orders for stocks and options, and more.
"""
from setuptools import setup

import ib


classifiers = """
Development Status :: 5 - Production/Stable
Intended Audience :: Developers
License :: OSI Approved :: BSD License
Natural Language :: English
Operating System :: OS Independent
Programming Language :: Python
Topic :: Office/Business :: Financial
Topic :: Office/Business :: Financial :: Investment
Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator
Topic :: Software Development :: Libraries
Topic :: Software Development :: Libraries :: Python Modules
"""


doclines = __doc__.split('\n')


setup(
    name='ib-python',
    version=ib.__version__,
    description=doclines[0],
    author='Ratson',
    author_email='contact@ratson.name',
    url='https://github.com/ratson/ib-python',
    license='BSD License',
    packages=['ib', 'ib/lib', 'ib/ext', 'ib/opt', 'ib/sym'],
    classifiers=filter(None, classifiers.split('\n')),
    long_description='\n'.join(doclines[2:]),
    platforms=['any'],
)
