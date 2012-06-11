'''
Copyright (c) 2012 Sven Reissmann <sven@0x80.io>

This file is part of the PyTgen traffic generator.

PyTgen is free software: you can redistribute it and/or modify it 
under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PyTgen is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PyTgen. If not, see <http://www.gnu.org/licenses/>.
'''

import setuptools

setuptools.setup(
    license='GNU GPLv3',

    name='PyTgen',
    version='0.2',

    author='Sven Reissmann',
    author_email='sven@0x80.io',

    url='http://git.0x80.io/git/PyTgen',

    description='A simple Traffic Generator written in Python',
    long_description=open('README').read(),
    keywords='PyTgen network traffic generator',

    packages=[
        'core'
    ],

    entry_points={
        'console_scripts' : [
            'PyTgen = run:main'
        ]
    },

    install_requires=[
        'ping >= 0.2',
        'pycrypto >= 2.3',
        'paramiko >= 1.7'
    ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: System :: Traffic Generation'
    ]
)
