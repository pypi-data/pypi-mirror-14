#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import stackFifoLifo

setup(
    name='stackFifoLifo',
    version=stackFifoLifo.__version__,
    packages=find_packages(),
    author="Pierre Lucas",
    author_email="pierre.lucas@altie.fr",
    description="Stack FIFO and LIFO",
    long_description=open('README.md').read(),
    # install_requires = ,  # dependancies (type list: ["gunicorn","docutils
    # >=0.3"])
    include_package_data=True,  # use MANIFEST.in
    url = 'http://github.com/oryxr/stackFifoLifo',  # official page of librarie
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Topic :: Communications",
    ],
    license= "GPL",
)
