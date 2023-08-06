# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os
import codecs
from setuptools import setup, find_packages

def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


VERSION = read("VERSION").strip()

REPO_URL = "https://github.com/predicthq/rfhq"

PYPI_README_NOTE = """\
.. note::

   For the latest source, discussions, bug reports, etc., please visit the `GitHub repository <{}>`_
""".format(REPO_URL)

LONG_DESCRIPTION = "\n\n".join([PYPI_README_NOTE, read("README.rst")])


setup(
    name='rfhq',
    version=VERSION,
    license='MIT',
    author='PredictHQ',
    author_email="developers@predicthq.com",
    long_description=LONG_DESCRIPTION,
    url=REPO_URL,
    packages=find_packages(exclude=('tests*',)),
    test_suite="nose.collector",
    setup_requires=[
        "nose==1.3.7"
    ],
    tests_require=[
        "six",
        "nose==1.3.7",
        "coverage==4.0.3",
        "mock==1.3.0",
    ],
    install_requires=[
        "Django>=1.8",
        "djangorestframework>=3",
        "inflection",
        "python-dateutil",
        "elasticsearch<2.0.0",
        "elasticsearch-dsl<2.0.0",
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
    ]
)
