#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='zaguan_inspector',
    version='0.1.0',
    author='Felipe Lerena',
    author_email='flerena@msa.com.ar',
    packages=['zaguan_inspector'],
    scripts=[],
    url='http://pypi.python.org/pypi/zaguan_inspector/',
    license='LICENSE.txt',
    description='Webkit inspector for Zaguan',
    long_description=open('README.txt').read(),
    install_requires=['zaguan>=2.2'],
)
