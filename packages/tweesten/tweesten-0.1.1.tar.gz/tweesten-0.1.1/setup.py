# -*- coding: utf-8 -*-
# Copyright © 2016 Raúl Benito <erre.benito@gmail.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

# Setup for Tweesten
'''Setup for Tweesten'''

# standard library imports
import os.path

# external library imports
from setuptools import setup

CLASSIFIERS = [
    'Intended Audience :: End Users/Desktop',
    'Environment :: Console',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python :: 3.4'
]

setup(
    name='tweesten',
    version='0.1.1',
    license='GNU GPL v3',
    description=('twitter bot to tweet a collage of album covers ' +
                 'based on your last.fm scrobbles'),
    long_description=('twitter bot to tweet a collage of album covers ' +
                      'based on your last.fm scrobbles'),
    classifiers=CLASSIFIERS,
    author='Raúl Benito',
    author_email='erre.benito@gmail.com',
    url='https://github.com/errebenito/tweesten',
    download_url='https://github.com/errebenito/tweesten/tarball/0.1',
    packages=['tweesten'],
    scripts=['scripts/tweesten.py'],
    install_requires=['tweepy>=3.5.0'],
)
