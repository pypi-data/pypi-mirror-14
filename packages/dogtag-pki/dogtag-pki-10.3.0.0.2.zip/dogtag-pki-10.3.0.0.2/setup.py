# Authors:
#     Christian Heimes <cheimes@redhat.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright (C) 2015 Red Hat, Inc.
# All rights reserved.
#
"""Dogtag client library

In order to build wheels the wheel and setuptools packages are required:

  $ sudo yum install python-wheel python-setuptools

The 'release' alias builds and uploads a source distribution and universal
wheel. The version and release number are taken from pki-core.spec file.

  $ python setup.py release

The 'packages' alias just creates the files locally:

  $ python setup.py packages

For a complete list of all available commands (except for aliases):

  $python setup.py --help-commands
"""

import re
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


VERSION = '10.3.0.0.2'

setup(
    author='Dogtag Certificate System Team',
    author_email='pki-devel@redhat.com',
    name='dogtag-pki',
    version=VERSION,
    description='Client library for Dogtag Certificate System',
    long_description="""\
This package contains the REST client for Dogtag PKI.

The Dogtag Certificate System is an enterprise-class open source
Certificate Authority (CA). It is a full-featured system, and has been
hardened by real-world deployments. It supports all aspects of certificate
lifecycle management, including key archival, OCSP and smartcard management,
and much more. The Dogtag Certificate System can be downloaded for free
and set up in less than an hour.""",
    license='GPL',
    keywords='pki x509 cert certificate',
    url='http://pki.fedoraproject.org/',
    packages=['pki', 'pki.cli'],
    requirements=['python-nss', 'requests', 'six'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Topic :: Security :: Cryptography',
    ],
)
