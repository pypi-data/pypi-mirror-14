#!/usr/bin/env python

import re
from setuptools import setup


def get_version(filename):
    with open(filename) as fh:
        metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", fh.read()))
        return metadata['version']


setup(
    name='recone',
    version=get_version('recone/version.py'),
    description='Framework to remote control a network of clients.',
    author='Tobias Bleiker and Dumeni Manatschal',
    url='https://github.com/tbleiker/recone',

    packages=[
        'recone',
        'recone.nodes',
    ],

    scripts=[
        'bin/recone',
    ],

    install_requires=[
        'pyzmq',
        'msgpack-python',
    ],

    setup_requires=[
        'pytest-runner',
    ],

    tests_require=[
        'pytest',
    ],

    classifiers = [
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Communications',
    ],
)
