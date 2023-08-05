#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from setuptools import setup, find_packages

from docs import getVersion


# Variables ===================================================================
changelog = open('CHANGES.rst').read()
long_description = "\n\n".join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
    changelog
])


# Actual setup definition =====================================================
setup(
    name='edeposit.amqp.ltp',
    version=getVersion(changelog),
    description="E-Deposit's AMQP binding to Long Time Preservation system.",
    long_description=long_description,
    url='https://github.com/edeposit/edeposit.amqp.ltp/',

    author='Edeposit team',
    author_email='edeposit@email.cz',

    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    license='MIT',

    packages=find_packages('src'),
    package_dir={'': 'src'},

    # scripts=[''],

    namespace_packages=['edeposit', 'edeposit.amqp'],
    include_package_data=True,
    zip_safe=False,
    install_requires=open("requirements.txt").read().splitlines(),
    extras_require={
        "test": [
            "pytest"
        ],
        "docs": [
            "sphinx",
            "sphinxcontrib-napoleon",
        ]
    },
)
