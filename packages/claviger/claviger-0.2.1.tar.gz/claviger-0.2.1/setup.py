#!/usr/bin/env python

import sys
from setuptools import setup

setup(
    name='claviger',
    version='0.2.1',
    description='Synchronizes remote SSH authorized_keys',
    long_description="{0:s}\n{1:s}". format(
                    open('README.rst').read(),
                    open('CHANGES.rst').read()),
    author='Bas Westerbaan',
    author_email='bas@westerbaan.name',
    url='http://github.com/bwesterb/claviger/',
    packages=['claviger', 'claviger.tests'],
    package_dir={'claviger': 'src'},
    package_data={'claviger': [
                    'config.schema.yml']},
    test_suite='claviger.tests',
    license='GPL 3.0',
    zip_safe=False,
    install_requires=['demandimport >=0.3.0',
                      'PyYAML',
                      'six',
                      'tarjan',
                      'jsonschema',
                            ],
    entry_points = {
        'console_scripts': [
                'claviger = claviger.main:entrypoint',
            ]
        },
    classifiers=[
        # TODO
            ]
    ),
