#!/usr/bin/env python
# encoding: utf-8

from __future__ import with_statement
from setuptools import setup

with open("README.md") as f:
    long_description = f.read()

setup(
    name="exception-slacker",
    version="0.1.1",
    description="Notify exceptions on slack",
    long_description=long_description,
    author="hassaku",
    author_email="hassaku.apps@gmail.com",
    url="https://github.com/hassaku/exception_slacker",
    py_modules=["exception_slacker"],
    include_package_data=True,
    install_requires=["slacker"],
    tests_require=["nose", "mock"],
    license="MIT",
    keywords="slack exception",
    zip_safe=False,
    classifiers=[]
)
