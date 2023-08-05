# Copyright 2013-2015 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You may not
# use this file except in compliance with the License. A copy of the License
# is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='aws-cloudhsm-cli',

    version='3.0.5',

    description='Command line interface to CloudHSM',
    long_description=long_description,

    url='http://aws.amazon.com/cloudhsm/',

    author='The CloudHSM Team',
    author_email='aws-cloudhsm-support@amazon.com',

    # Choose your license
    license='Apache License 2.0 http://aws.amazon.com/apache2.0/',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2 :: Only'
    ],

    packages=find_packages(exclude=['contrib', 'docs', 'test']),

    install_requires=['setuptools','boto>=2.27','pexpect>=2.4'],
    setup_requires=['nose>=1.0', 'mock>=1.0.1'],

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={
        'cloudhsmcli': ['endpoints.json', 'errorcodes.json']
    },
    include_package_data = True,

    data_files=[],

    entry_points={
        'console_scripts': [
            'cloudhsm=cloudhsmcli.main:main',
        ],
    },
)
