#!/usr/bin/env python3

import os, sys
from pprint import pprint

# IMPORTANT: We are simply importing, so it is going to get the *installed* version.  If you
# modify autoconfig.py you *must* run ``python setup.py install`` before testing.

# To use, simply import and call init.  The simplest use is to call with no parameters.

import autoconfig
autoconfig.init(env=['other', 'another', 'missing'])

# Let's see what was put into the environment.
e = list(os.environ.items())
e.sort()
pprint(e)

import logging
logger = logging.getLogger('main')
logger.info('INFO')
logger.warning('warning')
logger.error('error')
logger.debug('debug')
print('printed')

import sys
print('PATH:')
pprint(sys.path)

# We added libdir to the system path - make sure we can import packages from it.
import testlib
