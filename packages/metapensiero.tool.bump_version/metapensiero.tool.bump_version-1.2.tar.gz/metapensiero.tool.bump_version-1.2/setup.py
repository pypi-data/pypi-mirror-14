# -*- coding: utf-8 -*-
# :Project:   metapensiero.tool.bump_version -- Simple tool to bump a version number
# :Created:   dom  9 ago 2015, 14.28.40, CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: Copyright (C) 2015 Lele Gaifax
#

import os
from codecs import open

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.rst'), encoding='utf-8') as f:
    CHANGES = f.read()
with open(os.path.join(here, 'version.txt'), encoding='utf-8') as f:
    VERSION = f.read().strip()

setup(
    name="metapensiero.tool.bump_version",
    version=VERSION,
    url="https://bitbucket.org/lele/metapensiero.tool.bump_version",

    description="A simple tool to bump version number of a Python package",
    long_description=README + u'\n\n' + CHANGES,

    author="Lele Gaifax",
    author_email="lele@metapensiero.it",

    license="GPLv3+",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        "Programming Language :: Python",
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        ],
    keywords='',

    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['metapensiero', 'metapensiero.tool'],

    install_requires=['setuptools', 'Versio'],

    entry_points="""\
    [console_scripts]
    bump_version = metapensiero.tool.bump_version:main
    """,
)
