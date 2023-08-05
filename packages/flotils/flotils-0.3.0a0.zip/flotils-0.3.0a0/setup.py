#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from setuptools import setup


def get_version():
    import os
    import re
    version_file = os.path.join("flotils", "__init__.py")
    initfile_lines = open(version_file, 'rt').readlines()
    version_reg = r"^__version__ = ['\"]([^'\"]*)['\"]"
    for line in initfile_lines:
        mo = re.search(version_reg, line, re.M)
        if mo:
            return mo.group(1)
    raise RuntimeError(
        u"Unable to find version string in {}".format(version_file)
    )


def get_file(path):
    with open(path, 'r') as f:
        return f.read()


version = get_version()
readme = get_file("README.rst")
history = get_file("HISTORY.rst")
requirements = get_file("requirements.txt").split("\n")

assert version is not None
assert readme is not None
assert history is not None
assert requirements is not None

setup(
    name="flotils",
    version=version,
    description="Utility functions and classes",
    long_description=readme + "\n\n" + history,
    author="the01",
    author_email="jungflor@gmail.com",
    url="https://github.com/the01/python-flotils",
    packages=[
        "flotils"
    ],
    install_requires=requirements,
    license="MIT License",
    keywords="flotils logging wrapper loading json baseclass",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
    ]
)
