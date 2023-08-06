#!/usr/bin/env python
import sys
from setuptools import setup

if sys.version_info[0] >= 3:
    sys.exit('Sorry, Python 3.x is not supported')
if sys.version_info[0] == 2 and sys.version_info[1] < 7:
    sys.exit('Sorry, Python < 2.7 is not supported')
if sys.version_info[0] == 1:
    sys.exit('Sorry, Python 1.x is not supported')

setup(
    name='mookoo',
    version='0.1.0',
    description="Mock HTTP server",
    author='GaoRongxin',
    author_email='rongxin.gao@gmail.com',
    url='https://github.com/gaorx/mookoo/',
    license='MIT',
    platforms='any',
    packages=['mookoo'],
    package_data={
        '': ['help.html', 'README.md', 'LICENSE'],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    entry_points={
        'console_scripts': ['mookoo = mookoo:cli_entry'],
    },
)
