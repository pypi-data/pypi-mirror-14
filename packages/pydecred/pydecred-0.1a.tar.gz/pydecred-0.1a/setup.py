#!/usr/bin/env python

from setuptools import setup, find_packages
import os

version = '0.1a'
requires = ['decred_hash', 'python-bitcoinlib']

setup(
    name='pydecred',
    author='Tyler Willis',
    author_email='kefkiusrex@gmail.com',
    version=version,
    url='https://github.com/kefkius/pydecred',
    description='Decred python library.',
    keywords='decred',
    packages=find_packages(),
    install_requires=requires,
    test_suite='decred.tests'
)
