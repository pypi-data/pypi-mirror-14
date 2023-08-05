# -*- coding: utf-8 -*-
# :Project:   hurm -- Human Resources Manager
# :Created:   lun 14 dic 2015, 10.24.47, CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2015, 2016 Lele Gaifax
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

setup(
    name="hurm.db",
    version=VERSION,
    url="https://bitbucket.org/lele/hurm.db",

    description="Human Resources Manager, database definition",
    long_description=README + u'\n\n' + CHANGES,

    author="Lele Gaifax",
    author_email="lele@metapensiero.it",

    license="GPLv3+",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved ::"
        " GNU General Public License v3 or later (GPLv3+)",
        ],
    keywords='sqlalchemy postgresql',

    packages=['hurm.db'],
    namespace_packages=['hurm'],

    include_package_data=True,
    zip_safe=False,

    install_requires=[
        'cryptacular',
        'psycopg2',
        'setuptools',
        'sqlalchemy',
        'translationstring'
        ],
    extras_require={'dev': [
        'babel',
        'metapensiero.sphinx.patchdb',
        'metapensiero.sqlalchemy.dbloady',
        'metapensiero.tool.bump_version',
        'pyaxon',
        'readme',
    ]},
)
