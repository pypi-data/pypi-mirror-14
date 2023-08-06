#!/usr/bin/env python
from setuptools import setup, find_packages
import sys

long_description = ''

if 'upload' in sys.argv:
    with open('README.rst') as f:
        long_description = f.read()

version_info = sys.version_info

setup(
    name='metautils',
    version='0.1.2',
    description='Utilities for working with metaclasses.',
    author='Quantopian Inc.',
    author_email='opensource@quantopian.com',
    packages=find_packages(),
    long_description=long_description,
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ],
    url='https://github.com/quantopian/metautils',
    install_requires=['functools32'] if version_info.major == 2 else [],
    extras_require={
        'dev': ['nose==1.3.7'],
    },
)
