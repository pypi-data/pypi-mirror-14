#!/usr/bin/env python

from setuptools import setup, find_packages
import setuptools.command.install

setup(
    name="jw.badipsrbl",
    version="0.5.4",
    packages=find_packages(),
    install_requires=[
        'setuptools',
        'future',
        'jw.util',
        'gevent',
        'dnslib',
        'ipcalc'
    ],
    package_data={
        '': ['*.rst', '*.txt']
    },
    entry_points={
        'console_scripts': [
            'badipsrbl = jw.badips.main:Main'
        ]
    },
    test_suite='nose.collector',
    tests_require=['Nose'],
    author="Johnny Wezel",
    author_email="dev-jay@wezel.name",
    description="RBL DNS Server for badips.com",
    long_description='RBL DNS Server for badips.com',
    license="GPL 3",
    platforms='POSIX',
    keywords="rbl dns badips",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    url="https://pypi.python.org/pypi/jw.badipsrbl"
)
