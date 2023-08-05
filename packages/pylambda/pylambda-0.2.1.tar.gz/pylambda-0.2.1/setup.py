#!/usr/bin/env python
from setuptools import setup, find_packages
import os
import sys

requires = [
    'awscli'
]

setup(
    name='pylambda',
    version='0.2.1',
    description='Run your local python AWS Lambda locally and deploy to S3.',
    long_description=open('README.rst').read(),
    url='https://github.com/PitchBook/pylambda',
    author='Nicholas Ames',
    license='MIT',
    keywords='aws lambda s3',

    packages=find_packages(exclude=['test/*']),
    install_requires=requires,

    entry_points={
        'console_scripts': [
            'pylambda=pylambda:main',
        ],
    },

    extras_require={
        'test': ['coverage', 'mock', 'unittest2'],
    }
)
