#!/usr/bin/env python

# from distutils.core import setup
from setuptools import setup

setup(
    name='iampoliciesgonewild',
    packages=['iampoliciesgonewild'],
    version='1.0.5',
    description='AWS IAM Policy Expander Minimizer',
    author='Patrick Kelley',
    author_email='pkelley@netflix.com',
    url='https://github.com/monkeysecurity/iampoliciesgonewild',
    keywords = ['iam', 'policy', 'wildcard'],
    include_package_data=True
)
