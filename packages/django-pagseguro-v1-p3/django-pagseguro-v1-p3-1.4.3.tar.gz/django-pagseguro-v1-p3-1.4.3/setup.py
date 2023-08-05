#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
import sys
from setuptools import setup, find_packages
from django_pagseguro import __version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

setup(
    name='django-pagseguro-v1-p3',
    version=__version__,
    author='Gustavo Fonseca',
    author_email='contato@gustavofonseca.com.br',
    maintainer="Gustavo Fonseca",
    maintainer_email="contato@gustavofonseca.com.br",
    url='http://github.com/gustavoxpg/django-pagseguro',
    install_requires=[
        'Django>=1.9.2'
    ],
    description = 'A pluggable Django application for integrating PagSeguro payment system',
    long_description=open('README.rst').read(),
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        'Programming Language :: Python :: 3.5'
    ],
)
