#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
from os.path import dirname
from os.path import join
from setuptools import find_packages
from setuptools import setup

# requirements
with open('requirements.txt') as f:
    required = f.read().splitlines()

with open(join(dirname(__file__), 'pyrcmd3/VERSION'), 'rb') as f:
    version = f.read().decode('ascii').strip()

setup(
    name="pyrcmd3",
    version=version,
    description="Python3 Remote Commands toolkit",
    long_description=open('README.rst').read(),
    author="Marreta",
    author_email="coder@marreta.org",
    maintainer="Bruno Costa, Kairo Araujo",
    maintainer_email="coder@marreta.org",
    url="https://github.com/marreta/pyrcmd3/",
    keywords="Python3 Remote Command Commands SSH Toolkit",
    packages=find_packages(exclude=['*.test', 'tests.*']),
    package_data={'': ['license.txt', 'pyrcmd3/VERSION']},
    install_requires=required,
    include_package_data=True,
    license='BSD',
    platforms='Posix; MacOS X; Windows',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Topic :: System :: Shells',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
