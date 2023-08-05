# pylint: disable=W0622
"""cubicweb-fckeditorcompat application packaging information"""

modname = 'fckeditorcompat'
distname = 'cubicweb-fckeditorcompat'

numversion = (0, 1, 2)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
author = 'LOGILAB S.A. (Paris, FRANCE)'
author_email = 'contact@logilab.fr'
description = 'contains fckeditor 1:2.6.6-3 code'
web = 'http://www.cubicweb.org/project/%s' % distname

__depends__ =  {'cubicweb': '>= 3.18.0'}
__recommends__ = {}

classifiers = [
    'Environment :: Web Environment',
    'Framework :: CubicWeb',
    'Programming Language :: Python',
    'Programming Language :: JavaScript',
    ]

from os import listdir as _listdir, walk
from os.path import join, isdir
from glob import glob

THIS_CUBE_DIR = join('share', 'cubicweb', 'cubes', modname)

def listdir(dirpath):
    return [join(dirpath, fname) for fname in _listdir(dirpath)
            if fname[0] != '.' and not fname.endswith('.pyc')
            and not fname.endswith('~')
            and not isdir(join(dirpath, fname))]

def all_subdirs_of(dirpath):
    subdirs = []
    for root, dirs, files in walk(dirpath):
        subdirs.append(root)
    return tuple(subdirs)

data_files = [
    # common files
    [THIS_CUBE_DIR, [fname for fname in glob('*.py') if fname != 'setup.py']],
    ]
# check for possible extended cube layout
directories = ('data', 'wdoc', 'i18n', 'migration')
directories += all_subdirs_of('data') + all_subdirs_of('migration')
for dname in directories:
    if isdir(dname):
        data_files.append([join(THIS_CUBE_DIR, dname), listdir(dname)])
# Note: here, you'll need to add subdirectories if you want
# them to be included in the debian package

