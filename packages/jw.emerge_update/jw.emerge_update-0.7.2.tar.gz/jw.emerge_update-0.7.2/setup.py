#!/usr/bin/env python

# Copyright (c) 2015 Johnny Wezel
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup, find_packages
import setuptools.command.install

setup(
    name="jw.emerge_update",
    version="0.7.2",
    packages=find_packages(),
    install_requires=[
        'setuptools',
        'requests',
        'jw.util'
    ],
    package_data={
        '': ['*.rst', '*.txt']
    },
    entry_points={
        'console_scripts': [
            'emerge_update = jw.emerge_update.main:Main'
        ]
    },
    author="Johnny Wezel",
    author_email="dev-jay@wezel.name",
    description="Package maintenance (portage) and system management for Gentoo Linux",
    long_description=open('README.rst').read(),
    license="GPL",
    platforms='Linux',
    keywords="gentoo package maintenance",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ],
    url="https://pypi.python.org/pypi/emerge-update"
)
