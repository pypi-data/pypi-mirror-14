#!/usr/bin/env python
# (C) 2016, MIT License

'''
Installation configuration.
'''
from setuptools import setup

setup(
    name='bz2_rl',
    version='1.0.2',
    description=(
        'Helper class for processing large bzip2 compressed text files '
        'efficiently without high memory usage.'
    ),
    url='https://github.com/msikma/bz2_rl',
    author='Michiel Sikma',
    author_email='michiel@sikma.org',
    license='MIT',
    test_suite='bz2_rl.tests.test_bz2_rl',
    packages=['bz2_rl'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    zip_safe=True
)
