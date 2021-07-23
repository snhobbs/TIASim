#!/usr/bin/env python3
from setuptools import setup, find_packages
from glob import glob

with open("README.md", 'r') as f:
    LONG_DESCRIPTION = f.read()

setup(name='tiasim',
    version='0.0.1',
    description='Transimpedance Amplifier Simulation',
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author='Simon Hobbs',
    author_email='simon.hobbs@electrooptical.net',
    license='GPL-3.0',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux",
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy',
        'matplotlib'
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
    include_package_data=True,
    zip_safe=True)
