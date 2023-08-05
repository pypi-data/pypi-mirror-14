#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Pedro Tome <pedro.tome@idiap.ch>
#
# Copyright (C) 2015 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


from setuptools import setup, find_packages

# Define package version
version = open("version.txt").read().rstrip()

# The only thing we do in this file is to call the setup() function with all
# parameters that define our package.
setup(

    name='bob.db.verapalm',
    version=version,
    description='VERA Palmvein Database Access API for Bob',
    url='https://pypi.python.org/pypi/bob.db.verapalm',
    license='GPLv3',
    author='Pedro Tome',
    author_email='pedro.tome@idiap.ch',
    keywords='fingervein recognition, bob, bob.db, VERA',
    long_description=open('README.rst').read(),

    # This line is required for any distutils based packaging.
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,

    install_requires=[
      'setuptools',
      'six',  # py2/3 compatibility library
      'bob.io.base',
      'bob.db.base',
      'bob.db.verification.utils'
    ],

    namespace_packages = [
      'bob',
      'bob.db',
      ],

    entry_points = {
      # bob database declaration
      'bob.db': [
        'verapalm = bob.db.verapalm.driver:Interface',
        ],

      # bob unittest declaration
      'bob.test': [
        'verapalm = xbob.db.verapalm.test:VERAPalmDatabaseTest',
        ],
      },

    classifiers = [
      'Framework :: Bob',
      'Development Status :: 4 - Beta',
      'Environment :: Console',
      'Intended Audience :: Developers',
      'Intended Audience :: Education',
      'Intended Audience :: Science/Research',
      'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
      'Natural Language :: English',
      'Programming Language :: Python',
      'Programming Language :: Python :: 3',
      'Topic :: Scientific/Engineering :: Artificial Intelligence',
      'Topic :: Database :: Front-Ends',
      ],
)