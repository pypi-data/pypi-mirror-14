#------------------------------------------------------------------------------
#
#  Copyright (c) 2016, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in LICENSE.txt and may be redistributed only
#  under the conditions described in the aforementioned license.  The license
#  is also available online at http://www.enthought.com/licenses/BSD.txt
#
#  Thanks for using Enthought open source!
#
#------------------------------------------------------------------------------
# XXX: module copied from enstaller.plat
import platform
import sys


if '64' in platform.architecture()[0]:
    ARCH = 'amd64'
    BITS = 64
else:
    ARCH = 'x86'
    BITS = 32


def _guess_plat():
    sys_map = {'linux3': 'rh5', 'linux2': 'rh5', 'darwin': 'osx',
               'sunos5': 'sol', 'win32': 'win', 'linux': 'rh5'}
    try:
        return '%s-%d' % (sys_map[sys.platform], BITS)
    except KeyError:
        return None


try:
    from custom_tools import platform as CUSTOM_PLAT
except ImportError:
    CUSTOM_PLAT = _guess_plat()


SUBDIR_MAP = {
    'win-64': 'Windows/amd64',
    'win-32': 'Windows/x86',
    'osx-64': 'MacOSX/amd64',
    'osx-32': 'MacOSX/x86',
    'rh3-64': 'RedHat/RH3_amd64',
    'rh3-32': 'RedHat/RH3_x86',
    'rh5-64': 'RedHat/RH5_amd64',
    'rh5-32': 'RedHat/RH5_x86',
    'sol-64': 'Solaris/Sol10_amd64',
    'sol-32': 'Solaris/Sol10_x86',
}

SUBDIR = SUBDIR_MAP.get(CUSTOM_PLAT)
