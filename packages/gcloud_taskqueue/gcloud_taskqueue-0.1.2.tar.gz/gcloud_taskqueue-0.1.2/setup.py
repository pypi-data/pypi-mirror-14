#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ================================================================
# http://python-packaging-user-guide.readthedocs.org/en/latest/
# ================================================================

import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), "VERSION.txt"), "r") as fp:
    version = fp.read().strip()

with open(os.path.join(os.path.dirname(__file__), "CHANGES.txt"), "r") as fp:
    changes = fp.read().strip()

with open(os.path.join(os.path.dirname(__file__), "README.rst"), "r") as fp:
    readme = fp.read().strip()

long_description = "\n".join([readme, changes])

setup(
    name='gcloud_taskqueue',
    version=version,
    author='Bas van den Broek',
    author_email='cwasvandenbroek@gmail.com',
    url="https://github.com/sebastiancodes/gcloud_taskqueue",
    license='Apache License, Version 2.0',
    description='Interface for TaskQueue',
    long_description=long_description,
    zip_safe=True,
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='google-api-python-client google-gcloud gcloud google-taskqueue taskqueue',
    install_requires=[
        "gcloud"
    ],
)
