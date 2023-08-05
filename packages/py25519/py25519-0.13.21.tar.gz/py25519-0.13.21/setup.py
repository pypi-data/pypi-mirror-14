'''
    Python wrapper around curve25519 by mehdi sotoodeh.
    The files under py25519/c  are from mehdi sotoodeh and are copied
    unchanged from https://github.com/msotoodeh/curve25519.

    The files under py25519/c are licensed under the MIT LICENSE (see
    license.txt file under py25519/c).

    All remaining files in this package are licensed under the GNU
    General Public License version 3 or (at your option) any later version.

    See the file LICENSE-GPLv3.txt for details of the GNU General Public
    License version 3.

    Copyright (C) 2016  Sundar Nagarajan

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
import sys
import os
from setuptools import setup, find_packages, Extension
# Import setupext ONLY if you want custom triggers
# If you only use prep_cmd, you only need to include setupext in the package
# import setupext
# Import setupext IFF you use prep_cmd or want custom triggers
# import setupext


os.chdir(os.path.dirname(sys.argv[0]) or ".")

'''
==============================================================================
PACKAGE DATA
==============================================================================
'''
# You _SHOULD_ set these
name = 'py25519'
version = '0.13.21'   # oldver: '0.13.20'
url = 'https://github.com/sundarnagarajan/py25519'
download_url = '%s/tree/%s' % (url, version)
description = name
install_requires = [
    'cffi_utils',
]
packages = find_packages()
license = 'License :: OSI Approved :: MIT License'

# The following are optional
author = 'Sundar Nagarajan'
# author_email = ''
maintainer = author
# maintainer_email = author_email
classifiers = [
    'Development Status :: 4 - Beta',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: Implementation :: PyPy',
    'License :: OSI Approved :: MIT License',
    ('License :: OSI Approved :: '
     'GNU Lesser General Public License v3 or later (LGPLv3+)'
     )
]
zip_safe = True


'''
==============================================================================
C EXTENSION DETAILS
C source files are NOT under the python module, so that the
C files are NOT installed with the python module

Add c_dir to MANIFEST.in as graft
Add any dir with prep scripts to MANIFEST.in as graft
==============================================================================
'''
c_dir = 'c'
libname = 'libcurve25519'
c_src_files = [
    'source/curve25519_dh.c',
    'source/curve25519_mehdi.c',
    'source/curve25519_order.c',
    'source/curve25519_utils.c',
    'source/custom_blind.c',
    'source/ed25519_sign.c',
    'source/ed25519_verify.c',
    'source/sha512.c',
]
libpath = os.path.join(name, libname)
c_src_list = [os.path.join(c_dir, x) for x in c_src_files]

# ext_modules should be a LIST of dict - each dict is a
# set of keywords that define ONE extension. For a SINGLE extension
# ext_modules should be a LIST with a SINGLE dict
ext_modules = [
    dict(
        name=libpath,
        sources=c_src_list,
        include_dirs=[c_dir],
    )
]


'''
==============================================================================
ADDITIONAL DATA FILES
==============================================================================
'''

data_dirs = [
    'doc',
]


'''
==============================================================================
CUSTOM STEPS
To just execute a (shell) script to prepare C sources, call
set prep_cmd = STRING containing command with all args
Typically you will pass c_dir as a single argument to allow script to
cd c_dir and then execute prep steps

prepare_c_source will automatically set setupext.config and cmdclass
==============================================================================
'''
prep_cmd = os.path.join('prep/build.sh') + ' ' + c_dir

'''
==============================================================================
ADDITIONAL keyword args to setup() - shouldn't be required, normally
==============================================================================
'''
ADDL_KWARGS = dict(
)


'''
==============================================================================
           DO NOT CHANGE ANYTHING BELOW THIS
==============================================================================
'''


def prepare_c_source(cmd):
    '''
    cmd-->str: command with arguments
    '''
    import setupext
    setupext.config['build_ext']['pre']['cmdlist'] = [cmd]
    return setupext.get_cmdclass()


def get_longdesc(default=''):
    '''
    Returns-->str
    '''
    files = ['README.rst', 'README.md', 'README.txt', 'README']
    for f in files:
        try:
            return open(f, 'r').read()
        except:
            continue
    return default


def get_dirtree(topdir, dirlist=[]):
    '''
    topdir-->str: must be name of a dir under current working dir
    dirlist-->list of str: must all be names of dirs under topdir
    '''
    ret = []
    curdir = os.getcwd()
    if not os.path.isdir(topdir):
        return ret
    os.chdir(topdir)
    try:
        for dirname in dirlist:
            if not os.path.isdir(dirname):
                continue
            for (d, ds, fs) in os.walk(dirname):
                for f in fs:
                    ret += [os.path.join(d, f)]
        return ret
    except:
        return ret
    finally:
        os.chdir(curdir)

# Make some keywords MANDATORY
for k in [
    'name', 'version', 'description', 'license',
]:
    if k not in locals():
        raise Exception('Missing mandatory keyword: ' + k)

# keywords that are computed from variables
dirlist = locals().get('data_dirs', None)
if isinstance(dirlist, list):
    package_dir = {name: name}
    package_data = {name: get_dirtree(topdir=name, dirlist=dirlist)}

long_description = get_longdesc(description)

known_keywords = [
    'name', 'version', 'packages', 'description', 'license',
    'install_requires', 'requires', 'setup_requires',
    'package_dir', 'package_data',
    'zip_safe', 'classifiers', 'keywords',
    'long_description', 'url', 'download_url',
    'author', 'author_email', 'maintainer', 'maintainer_email',
]

kwdict = {}
for k in known_keywords:
    if k in locals():
        kwdict[k] = locals()[k]

if 'prep_cmd' in locals():
    kwdict['cmdclass'] = prepare_c_source(locals()['prep_cmd'])

# Do not compile ext_modules during build phase - wasteful
if len(sys.argv) > 1 and sys.argv[1] != 'build':
    if 'ext_modules' in locals():
        kwdict['ext_modules'] = [Extension(**x) for x in
                                 locals()['ext_modules']]

# Additional keywords specified by user - shouldn't be required, normally
kwdict.update(ADDL_KWARGS)
setup(**kwdict)
