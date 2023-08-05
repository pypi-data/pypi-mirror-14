import sys
import os
from setuptools import setup, find_packages, Extension


os.chdir(os.path.dirname(sys.argv[0]) or ".")

'''
==============================================================================
PACKAGE DATA
==============================================================================
'''
# You _SHOULD_ set these
name = 'poly1305_donna'
version = '0.11.13'   # oldver: '0.11.12'
url = 'https://github.com/sundarnagarajan/py_poly1305-donna'
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
]
zip_safe = True


'''
==============================================================================
C EXTENSION DETAILS
==============================================================================
'''
c_dir = 'floodberry.poly1305_donna'
libname = 'libpoly1305donna'
c_src_files = [
    'poly1305-donna.c',
]
libpath = os.path.join(name, libname)
c_src_list = [os.path.join(c_dir, x) for x in c_src_files]
ext_modules = [
    Extension(
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
    'floodberry.poly1305_donna',
]


'''
==============================================================================
ADDITIONAL keyword args to setup() - should not be required, normally
==============================================================================
'''
ADDL_KWARGS = dict(
)


'''
==============================================================================
           DO NOT CHANGE ANYTHING BELOW THIS
==============================================================================
'''


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
    'ext_modules', 'package_dir', 'package_data',
    'zip_safe', 'classifiers', 'keywords',
    'long_description', 'url', 'download_url',
    'author', 'author_email', 'maintainer', 'maintainer_email',
]

kwdict = {}
for k in known_keywords:
    if k in locals():
        kwdict[k] = locals()[k]

# Additional keywords specified by user - shouldn't be required, normally
kwdict.update(ADDL_KWARGS)


setup(**kwdict)
