"""
Copyright 2016 Gu Zhengxiong <rectigu@gmail.com>

This file is part of BinTut.

BinTut is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

BinTut is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with BinTut.  If not, see <http://www.gnu.org/licenses/>.
"""


from setuptools import setup, find_packages


__author__ = 'Gu Zhengxiong'
__version__ = '0.2.0'

PROGRAM_NAME = 'BinTut'
PACKAGE_NAME = 'bintut'


with open('requirements.txt') as stream:
    requirements = stream.read().splitlines()


setup(
    name=PROGRAM_NAME,
    version=__version__,
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'bintut={name}.main:main'.format(name=PACKAGE_NAME)
        ]
    },

    author=__author__,
    author_email='rectigu@gmail.com',
    description='Teach You A Binary Exploitation For Great Good.',
    license='GPL-3',
    keywords='Classical Binary Exploitation',
    url='https://github.com/NoviceLive/' + PACKAGE_NAME,

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: '
        'GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
    ]
)
