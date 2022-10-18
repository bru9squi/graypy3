#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""setup.py for graypy"""

import codecs
import re
import sys
import os

from setuptools import setup, find_packages
from setuptools.command.test import test


def find_version(*file_paths):
    with codecs.open(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), *file_paths), "r"
    ) as fp:
        version_file = fp.read()
    m = re.search(r"^__version__ = \((\d+), ?(\d+), ?(\d+)\)", version_file, re.M)
    if m:
        return "{}.{}.{}".format(*m.groups())
    raise RuntimeError("Unable to find a valid version")


VERSION = find_version("graypy", "__init__.py")


class Pylint(test):
    def run_tests(self):
        from pylint.lint import Run

        Run(
            [
                "graypy",
                "--persistent",
                "y",
                "--rcfile",
                ".pylintrc",
                "--output-format",
                "colorized",
            ]
        )


class PyTest(test):
    user_options = [("pytest-args=", "a", "Arguments to pass to pytest")]

    def initialize_options(self):
        test.initialize_options(self)
        self.pytest_args = "-v --cov={}".format("graypy")

    def run_tests(self):
        import shlex

        # import here, cause outside the eggs aren't loaded
        import pytest

        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


setup(
    name="graypy",
    version=VERSION,
    description="Python logging handlers that send messages in the Graylog Extended Log Format (GELF).",
    long_description=open("README.rst").read(),
    long_description_content_type="text/x-rst",
    keywords="logging gelf graylog2 graylog udp amqp",
    author="Sever Banesiu",
    author_email="banesiu.sever@gmail.com",
    url="https://github.com/severb/graypy",
    license="BSD License",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    tests_require=[
        "pytest",
        "pytest-cov",
        "pylint",
        "mock",
        "requests",
        "amqp>=2.5.2",
        "black",
    ],
    extras_require={
        "amqp": ["amqp>=2.5.2"],
        "docs": [
            "sphinx",
            "sphinx_rtd_theme",
            "sphinx-autodoc-typehints",
        ],
    },
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: System :: Logging",
    ],
    cmdclass={"test": PyTest, "lint": Pylint},
)
