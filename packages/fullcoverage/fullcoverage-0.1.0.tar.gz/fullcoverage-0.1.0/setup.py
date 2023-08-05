#!/usr/bin/env python3

# Copyright 2014-2015 Louis Paternault
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

"""Installer"""

from setuptools import setup, find_packages
import codecs
import os

def readme():
    directory = os.path.dirname(os.path.join(
        os.getcwd(),
        __file__,
        ))
    with codecs.open(
        os.path.join(directory, "README.rst"),
        encoding="utf8",
        mode="r",
        errors="replace",
        ) as file:
        return file.read()

setup(
        name='fullcoverage',
        version="0.1.0",
        packages=find_packages(exclude=["test*"]),
        setup_requires=["hgtools"],
        install_requires=[
            'coverage',
            ],
        include_package_data=True,
        author='Louis Paternault',
        author_email='spalax@gresille.org',
        description='Cheat and get 100% test coverage',
        url='http://git.framasoft.org/spalax/fullcoverage',
        license="GPLv3 or any later version",
        test_suite="test.suite",
        classifiers=[
            "Development Status :: 4 - Beta",
            "Environment :: Plugins",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3 :: Only",
            "Programming Language :: Python :: 3.5",
            "Topic :: Software Development :: Testing",
        ],
        long_description=readme(),
        zip_safe = True,
)
