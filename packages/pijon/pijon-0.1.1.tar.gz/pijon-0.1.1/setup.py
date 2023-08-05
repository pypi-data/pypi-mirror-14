#!/usr/bin/env python

from setuptools import setup, find_packages


with open('VERSION.txt', 'r') as v:
    version = v.read().strip()

with open('DESCRIPTION', 'r') as d:
    long_description = d.read()

setup(
    name='pijon',
    description='Tool and library to help with json based schema and data migration.',
    long_description=long_description,
    url='http://www.surycat.com',
    author='Optiflows R&D',
    author_email='rand@surycat.com',
    version=version,
    packages=find_packages(exclude=['tests']),
    license='Apache 2.0',
    scripts=['scripts/pijon'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
    ],
)
