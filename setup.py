#! /usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

from lora import __version__

setup(
    name='lora',
    version=__version__,
    description='Package for interacting with Lorenz REST API',
    author='Ian Lee',
    author_email='lee1001@llnl.gov',
    url='https://github.com/llnl/python-lora',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
)
