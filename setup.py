#!/usr/bin/env python

from __future__ import print_function

import os
import subprocess
import sys
from pathlib import Path

import pypandoc

try:
    from setuptools import find_packages, setup
except ImportError:
    from distutils.core import find_packages, setup

directory = Path(__file__).resolve().parent

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 7)

if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.exit("Sorry, Python {}.{}+ is required".format(*REQUIRED_PYTHON))

def write_version_py():
    with open(os.path.join("dataramp", "version.txt")) as f:
        version = f.read().strip()

    try:
        git_revision = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip()
        # version += f".dev{git_revision}"
        version += f"+dev.{git_revision}"
    except subprocess.CalledProcessError:
        pass  # Handle the exception or leave it as is if git command fails

    # To write version info to dataramp/version.py
    with open(os.path.join("dataramp", "version.py"), "w") as f:
        f.write(f'__version__ = "{version}"\n')
    return version

def read_file(path):
    # if this fails on windows then add the following environment variable (PYTHONUTF8=1)
    with open(path, encoding='utf-8') as contents:
        return contents.read()

# Read the contents of the requirements_dev file
def list_reqs(fname='requirements_dev.txt'):
    return read_file(fname).splitlines()

# Convert Markdown to RST for PyPI
# Credits: http://stackoverflow.com/a/26737672

try:
    pypandoc_func = (
        pypandoc.convert_file if hasattr(pypandoc, "convert_file") else pypandoc.convert
    )
    long_description = pypandoc_func("README.md", "rst")
except (IOError, ImportError, OSError):
    long_description = read_file("README.md")

setup(
    name="Dataramp",
    version=write_version_py(),
    license="MIT",
    description="A Data science library for data science / data analysis teams",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Meshack Kitonga",
    author_email="kitongameshack9@gmail.com",
    url="",
    keywords=["Dataramp", "Data Science", "Data Analysis"],
    packages=find_packages(exclude=("tests",)),
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
)
