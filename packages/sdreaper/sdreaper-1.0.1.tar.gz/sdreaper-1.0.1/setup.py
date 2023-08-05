"""
|Downloads|

sdreaper
========

CLI that communicates with Arduino Reaper to pull files off an SD card and
delete them using a Serial connection.

.. |Downloads| image:: https://img.shields.io/pypi/dm/sdreaper.svg
   :target: https://pypi.python.org/pypi/sdreaper

"""
import os
import sys

from setuptools import setup, find_packages

setup(
    name='sdreaper',
    version='1.0.1',
    description='CLI and curses UI for talking to Arduino Reaper library',
    long_description=__doc__,
    url='https://github.com/humulabs/reaper/blob/master/README.md',
    author='Michael Keirnan',
    author_email='michael@keirnan.com',
    packages=['sdreaper'],
    package_dir={'': '.'},
    install_requires=[
        'pyserial',
        'docopt',
        'urwid_timed_progress',
    ],
    entry_points={
        'console_scripts': ['sdreaper=sdreaper.main:main'],
    },
    tests_require=[
        'mock',
        'pep8',
        'pytest',
    ],
    platforms='any',
    license='MIT',
    keywords="arduino iot sd serial",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Topic :: Home Automation',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ]
)
