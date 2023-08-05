#!/usr/bin/env python3
# -*- coding: ascii -*-
from __future__ import division, with_statement
from setuptools import setup, find_packages
import sys
import io

version = '1.2.0'
author = "Omoto Kenji"
license = "MIT License"
author_email = 'doloopwhile@gmail.com'


with io.open('README.rst', encoding='ascii') as fp:
    long_description = fp.read()

install_requires = ["six"]
if sys.version_info < (2, 7):
    install_requires = "argparse ordereddict".split()

setup(
    packages=find_packages(),
    include_package_data=True,
    name='PyExecJS',
    version=version,
    description='Run JavaScript code from Python',
    long_description=long_description,
    author=author,
    author_email=author_email,
    url='https://github.com/doloopwhile/PyExecJS',
    license=license,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: JavaScript',
    ],
    install_requires=install_requires,
    test_suite="test_execjs",
)
