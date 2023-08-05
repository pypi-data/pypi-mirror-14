#!/usr/bin/python
# -*- coding: utf-8 -*-

""""
Copyright (c) 2014, Matt Doiron. All rights reserved.

BTCnDash is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

BTCnDash is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with BTCnDash. If not, see <http://www.gnu.org/licenses/>.
"""

# Prepare for Python 3
from __future__ import (print_function, division, absolute_import)

# System imports
import os
import re
from codecs import open
from setuptools import setup

project = 'btcndash'
packages = ['btcndash']
requires = [
    "python-bitcoinlib==0.5.1",
    "bottle==0.12.9"
]
requires_extra = {
    'doc': ["sphinx==1.3.3"]
}

with open(os.path.join(project, '__init__.py'), 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)
    if not version:
        raise RuntimeError('Cannot find version information')
with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()
with open('CHANGELOG.rst', 'r', 'utf-8') as f:
    changelog = f.read()


setup(
    name=project,
    version=version,
    author='Matt Doiron',
    author_email='mattdoiron@gmail.com',
    url='https://bitbucket.org/mattdoiron/btcndash',
    download_url='https://bitbucket.org/mattdoiron/btcndash/downloads/',
    description='Lightweight status dashboard for Bitcoin nodes.',
    long_description=readme + '\n\n' + changelog,
    keywords='bitcoin node dashboard fullnode',
    packages=packages,
    platforms='any',
    license='GPL3',
    zip_safe=False,
    install_requires=requires,
    include_package_data=True,
    extras_require=requires_extra,
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
    entry_points={
        'console_scripts': ['btcndash = btcndash.btcndash:main']
    }
)
