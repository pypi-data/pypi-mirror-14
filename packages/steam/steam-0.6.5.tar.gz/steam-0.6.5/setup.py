#!/usr/bin/env python

from setuptools import setup, find_packages
from codecs import open
from os import path
import sys

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()
with open(path.join(here, 'steam/__init__.py'), encoding='utf-8') as f:
    __version__ = f.readline().split('"')[1]

install_requires = [
    'requests>=2.9.1',
    'vdf>=1.10',
    'pycrypto>=2.6.1',
    'gevent>=1.1rc3',
    'gevent-eventemitter>=1.2',
    'protobuf>=2.6.1',
]

if sys.version_info < (3, 4):
    install_requires.append('enum34>=1.0.4')

setup(
    name='steam',
    version=__version__,
    description='Module for interacting with various Steam features',
    long_description=long_description,
    url='https://github.com/ValvePython/steam',
    author="Rossen Georgiev",
    author_email='rossen@rgp.io',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Natural Language :: English',
        'Operating System :: OS Independent',
    ],
    keywords='valve steam steamid api webapi',
    packages=['steam'] + ['steam.'+x for x in find_packages(where='steam')],
    install_requires=install_requires,
    zip_safe=True,
)
