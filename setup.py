#!/usr/bin/env python3

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='compoundfin',
    version='0.1.0',
    description='Tool for tracking and analysing spending',
    long_description=readme,
    author='Ezra Savard, Lise Savard',
    author_email='git@ezrasavard.com',
    url='https://github.com/ezrasavard/compound',
    license=license,
    packages=find_packages(exclude=('tests'))
)
