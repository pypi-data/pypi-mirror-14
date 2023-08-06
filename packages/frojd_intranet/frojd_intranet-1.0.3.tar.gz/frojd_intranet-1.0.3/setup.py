#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import pip

from setuptools import setup, find_packages
from pip.req import parse_requirements


if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()

package_exclude = ("tests*", "examples*")
packages = find_packages(exclude=package_exclude)

# Install dependencies
requires = parse_requirements("requirements/install.txt",
                              session=pip.download.PipSession())
install_requires = [str(ir.req) for ir in requires]

# Convert markdown to rst
try:
    from pypandoc import convert
    long_description = convert("README.md", "rst")
except:
    long_description = ""


setup(
    name="frojd_intranet",
    version='1.0.3',
    description=("CLI tool for the frojd intranet"),
    long_description=long_description,
    author="Fröjd",
    author_email="martin.sandstrom@frojd.se",
    url="http://frojd.se",
    packages=packages,
    include_package_data=True,
    install_requires=install_requires,
    license="MIT",
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "frojd-intranet = frojd_intranet.main:main",
        ]
    },
)
