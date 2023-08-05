#!/usr/bin/env python3

# IMPORTANT: We are simply importing, so it is going to get the *installed* version.  If you
# modify autoconfig.py you *must* run ``python setup.py install`` before testing.

import os, sys, logging, os.path

# We want to run the version in the directory above is, so we'll modify the sys.path
sys.path.insert(0, os.path.abspath('..'))

envbefore = set(os.environ.keys())

# To use, simply import and call init.  The simplest use is to call with no parameters.
import autoconfig
autoconfig.init(env=['other', 'another', 'missing'])

# Let's see what was put into the environment.
envafter = set(os.environ.keys())
newkeys  = list(envafter - envbefore)
newkeys.sort()
print('New environment variables:', ' '.join(newkeys))

#
print()

logger = logging.getLogger('main')
logger.info('INFO')
logger.warning('warning')
logger.error('error')
logger.debug('debug')
print('printed')

print()
print('Loggers that are set to DEBUG:', logging.Logger.manager.loggerDict.keys())

import sys
print('\nPATH:')
for dir in sys.path:
    print(' ', dir)

# We added libdir to the system path - make sure we can import packages from it.
import testlib
