#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of python-escpos-xml.  The COPYRIGHT file at the top level
# of this repository contains the full copyright notices and license terms.
from setuptools import setup, find_packages
import os
import re
import codecs


def read(fname):
    return codecs.open(
        os.path.join(os.path.dirname(__file__), fname), 'r', 'utf-8').read()


def get_version():
    init = read(os.path.join('escpos_xml', '__init__.py'))
    return re.search("__version__ = '([0-9.]*)'", init).group(1)

setup(name='python-escpos-xml',
    version=get_version(),
    description='Print XML defined receipt on ESC/POS Printer',
    long_description=read('README'),
    author='B2CK',
    author_email='info@b2ck.com',
    url='http://hg.b2ck.com/python-escpos-xml/',
    packages=find_packages(),
    package_data={
        'escpos_xml': ['escpos.rnc', 'escpos.rng'],
        'escpos_xml.tests': ['image.xml'],
        },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Office/Business :: Financial',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    license='LGPL-3',
    install_requires=[
        'python-escpos',
        ],
    test_suite='escpos_xml.tests',
    tests_require=['mock'],
    )
