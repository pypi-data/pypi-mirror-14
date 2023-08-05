#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os import path
import io

here = path.abspath(path.dirname(__file__))

NAME = "barchart-ondemand-client-python"
with io.open(path.join(here, "barchart", "version.py"), "rt", encoding="UTF-8") as f:
    exec(f.read())

setup(
    name=NAME,
    version=__version__,
    description="A Python library to get data from BarChartOnDemand API",
    long_description="README.rst",
    url=__url__,
    author=__author__,
    author_email=__email__,
    license=__license__,

    classifiers=[
        "Development Status :: 4 - Beta",

        "Environment :: Console",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",

        "Programming Language :: Cython",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",

        "License :: OSI Approved :: MIT License",
    ],

    keywords="BarChartOnDemand python trading data client interface",

    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
    install_requires=[
        "python-dateutil",
        "requests",
        "requests-cache",
        "six"
    ],
    extras_require={
        "dev": ["check-manifest", "pytest"],
        "test": ["coverage", "pytest"],
    },

    package_data={
        "samples": ["samples/*.py"],
    },
)
