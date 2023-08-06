# -*- coding: utf-8 -*-
# Copyright (C) 2016 Ludia Inc.
# This software is licensed as described in the file LICENSE, which
# you should have received as part of this distribution.
# Author: Pior Bastida <pbastida@ludia.com>

from setuptools import setup, find_packages
import codecs

version = '0.1'


def read(filename):
    return unicode(codecs.open(filename, encoding='utf-8').read())

long_description = '\n\n'.join([read('README.rst'), read('CHANGES.rst')])

setup(
    name='dogpile_elasticache',
    version=version,
    description="Dogpile backend for AWS Elasticache Memcache service",
    long_description=long_description,
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ],
    keywords='dogpile cache aws elasticache memcache',
    author='Pior Bastida',
    author_email='pbastida@ludia.com',
    url='https://github.com/ludia/dogpile_elasticache',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'dogpile.cache',
        'pymemcache',
    ],
    extras_require={
        'test': ['nose', 'nosexcover', 'mock', 'zest.releaser[recommended]'],
        },
    entry_points={
        'dogpile.cache': [
            'elasticache_pymemcache = '
            'dogpile_elasticache.backends:ElasticachePyMemcacheBackend',
        ],
    },
)
