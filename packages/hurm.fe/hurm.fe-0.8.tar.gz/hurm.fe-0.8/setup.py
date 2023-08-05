# -*- coding: utf-8 -*-
# :Project:   hurm -- Package setup
# :Created:   lun 01 feb 2016 20:08:25 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016 Lele Gaifax
#

from io import open
import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.rst'), encoding='utf-8') as f:
    CHANGES = f.read()
with open(os.path.join(here, 'version.txt'), encoding='utf-8') as f:
    VERSION = f.read().strip()

requires = [
    'babel',
    'cryptacular',
    'metapensiero.extjs.desktop',
    'metapensiero.sqlalchemy.proxy',
    'pyramid',
    'pyramid_tm',
    'pyyaml',
    'reportlab',
    'setuptools',
    'sqlalchemy',
    'transaction',
    'waitress',
    'xlwt',
    'zope.sqlalchemy',
    ]

setup(
    name='hurm.fe',
    version=VERSION,
    description='Human Resources Manager, ExtJS frontend',
    long_description=README + '\n\n' + CHANGES,

    license="GPLv3+",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Programming Language :: JavaScript",
        "Operating System :: OS Independent",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved ::"
        " GNU General Public License v3 or later (GPLv3+)",
    ],
    author='Lele Gaifax',
    author_email='lele@metapensiero.it',
    url='https://bitbucket.org/lele/hurm.fe',
    keywords='web wsgi bfg pylons pyramid',

    packages=['hurm.fe'],
    namespace_packages=['hurm'],

    include_package_data=True,
    zip_safe=False,

    install_requires=requires,
    extras_require={'dev': ['metapensiero.tool.bump_version', 'readme']},

    entry_points="""\
    [paste.app_factory]
    main = hurm.fe:main
    """,
)
