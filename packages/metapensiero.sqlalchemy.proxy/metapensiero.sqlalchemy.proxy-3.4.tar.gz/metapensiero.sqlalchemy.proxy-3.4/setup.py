# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.proxy
# :Created:   mar 11 ago 2009 14:18:40 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2009, 2010, 2012, 2013, 2014, 2015, 2016 Lele Gaifax
#

from io import open
import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.rst'), encoding='utf-8') as f:
    CHANGES = f.read()
with open(os.path.join(here, 'version.txt'), encoding='utf-8') as f:
    VERSION = f.read().strip()

setup(
    name='metapensiero.sqlalchemy.proxy',
    version=VERSION,
    description="Expose SQLAlchemy's queries and their metadata to a webservice",
    long_description=README + u'\n\n' + CHANGES,

    author='Lele Gaifax',
    author_email='lele@metapensiero.it',
    url="https://bitbucket.org/lele/metapensiero.sqlalchemy.proxy",

    license="GPLv3+",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved ::"
        " GNU General Public License v3 or later (GPLv3+)",
        "Topic :: Database",
    ],

    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['metapensiero', 'metapensiero.sqlalchemy'],

    install_requires=[
        'setuptools',
        'nssjson',
        'sqlalchemy',
    ],
    extras_require={'dev': ['metapensiero.tool.bump_version', 'readme']},
)
