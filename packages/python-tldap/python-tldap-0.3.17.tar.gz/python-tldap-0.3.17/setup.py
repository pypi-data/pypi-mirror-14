#!/usr/bin/env python

# Copyright 2012-2014 Brian May
#
# This file is part of python-tldap.
#
# python-tldap is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# python-tldap is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with python-tldap  If not, see <http://www.gnu.org/licenses/>.

import os
from setuptools import setup

with open('VERSION.txt', 'r') as f:
    version = f.readline().strip()

os.environ['DJANGO_SETTINGS_MODULE'] = 'tldap.tests.settings'

setup(
    name="python-tldap",
    version=version,
    url='https://github.com/Karaage-Cluster/python-tldap',
    author='Brian May',
    author_email='brian@v3.org.au',
    description='High level python LDAP Library',
    packages=[
        'tldap', 'tldap.test', 'tldap.backend',
        'tldap.methods', 'tldap.tests', 'tldap.schemas',
        'tldap.test.ldap_schemas',
        'tldap.methods.south_migrations', 'tldap.methods.migrations'],
    license="GPL3+",
    long_description=open('README.rst').read(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: "
            "GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="ldap django",
    package_data={
        'tldap.test.ldap_schemas': ['*.schema', ],
    },
    install_requires=[
        "django",
        "ldap3",
        "passlib",
        "six",
    ],
    test_suite="tldap.tests",
)
