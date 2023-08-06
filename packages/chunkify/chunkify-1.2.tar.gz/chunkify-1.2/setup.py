#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name="chunkify",
    version="1.2",
    description=" Python module to split an iterable into a certain number of chunks",
    author="Ben Hearsum",
    author_email="ben@hearsum.ca",
    url="https://github.com/bhearsum/chunkify",
    packages=["chunkify"],
    license="MPL",
)
