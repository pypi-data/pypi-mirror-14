#!/usr/bin/env python
# (C) 2016, MIT License

'''
Installation configuration.
'''
from setuptools import setup, find_packages

setup(
    name='bz2_rl',
    version='2.0.0',
    description=(
        'Helper class for processing large bzip2 compressed text files '
        'efficiently without high memory usage.'
    ),
    url='https://github.com/msikma/bz2_rl',
    author='Michiel Sikma',
    author_email='michiel@sikma.org',
    license='MIT',
    test_suite='bz2_rl.tests',
    packages=find_packages(),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    zip_safe=True
)
