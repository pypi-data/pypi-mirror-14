#!/usr/bin/env python
# encoding: UTF-8

from setuptools import setup, find_packages

setup(
    name='rcpp',
    version='1.0',
    keywords=['g++', 'cpp', 'cli', 'run'],
    description="auto run cpp file",
    license='MIT License',
    packages=find_packages(),

    include_package_data=True,

    entry_points={
        'console_scripts': [
            'rcpp = rcpp:start'
        ],
    },

    author='ahonn',
    author_email='ahonn95@outlook.com',
    zip_safe=False,
)
