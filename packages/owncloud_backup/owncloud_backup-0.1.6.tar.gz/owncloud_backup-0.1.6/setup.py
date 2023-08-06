#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from setuptools import setup


# Parser ======================================================================
def getVersion(data):
    """
    Parse version from changelog written in RST format.
    """
    def allSame(s):
        return not any(filter(lambda x: x != s[0], s))

    def hasDigit(s):
        return any(char.isdigit() for char in s)

    data = data.splitlines()
    return next((
        v for v, u in zip(data, data[1:])  # v = version, u = underline
        if len(v) == len(u) and allSame(u) and hasDigit(v) and "." in v
    ))


# Variables ===================================================================
CHANGELOG = open('CHANGELOG.rst').read()
LONG_DESCRIPTION = "\n\n".join([
    open('README.rst').read(),
    CHANGELOG
])


# Actual setup definition =====================================================
setup(
    name='owncloud_backup',
    version=getVersion(CHANGELOG),
    description="backupper for uploading and managing files in ownCloud.",
    long_description=LONG_DESCRIPTION,
    url='https://github.com/NLCR/owncloud_backup',

    author='Bystroushaak',
    author_email='bystrousak[at]kitakitsune.org',

    classifiers=[
        "Development Status :: 3 - Alpha",

        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",

        "Intended Audience :: Developers",

        "License :: OSI Approved :: MIT License",
    ],
    license='MIT',

    py_modules=["owncloud_backup"],
    scripts=[
        "owncloud_backup.py"
    ],

    include_package_data=True,
    zip_safe=True,

    install_requires=open("requirements.txt").read().splitlines(),
    extras_require={
        "test": ["pytest"],
    }
)
