#!/usr/bin/env python

from distutils.core import setup

setup(
    name='autoconfig',
    description='Simple environment, logging, and sys.path setup from a config file',
    version='1.1.0',
    py_modules=['autoconfig'],
    author='Michael Kleehammer',
    author_email='<michael@kleehammer.com>',
    url='http://github.com/mkleehammer/autoconfig',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development'
    ]
)
