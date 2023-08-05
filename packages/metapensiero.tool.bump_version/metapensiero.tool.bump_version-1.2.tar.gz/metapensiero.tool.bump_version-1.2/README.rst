.. -*- coding: utf-8 -*-
.. :Project:   metapensiero.tool.bump_version -- Simple tool to bump a version number
.. :Created:   dom  9 ago 2015, 14.28.40, CEST
.. :Author:    Lele Gaifax <lele@metapensiero.it>
.. :License:   GNU General Public License version 3 or later
.. :Copyright: Copyright (C) 2015, 2016 Lele Gaifax
..

================================
 metapensiero.tool.bump_version
================================

A simple tool to bump version number of a Python package
========================================================

 :author: Lele Gaifax
 :contact: lele@metapensiero.it
 :license: GNU General Public License version 3 or later

This is a very simple tool that I use to automatize the management of the ``version.txt`` file
I usually put in my Python packages. There are tons of equivalent tools around, but none of
them fullfilled my needs.

It uses the package `Versio`__ to handle different versioning schemas, with an additional
``simple2`` scheme for versions composed simply by `major.minor` numbers.

__ https://pypi.python.org/pypi/Versio

Examples::

  $ echo "0.0" > version.txt
  $ bump_version --dry-run
  Old version: 0.0
  New version: 0.1

  $ bump_version -n --field major
  Old version: 0.0
  New version: 1.0

  $ echo "0.0.0.0" > version.txt
  $ bump_version -f minor --scheme simple4
  $ cat version.txt
  0.1.0.0

  $ echo "0.9" > version.txt
  $ bump_version -n -f release --index 1 -s pep440
  Old version: 0.9
  New version: 0.10

  $ bump_version -f release -i 1 -s pep440
  $ cat version.txt
  0.10

  $ bump_version -n -f pre -i 1 -s pep440
  Old version: 0.10
  New version: 0.10a1

  $ bump_version -n -f post -i 1 -s pep440
  Old version: 0.10
  New version: 0.10.post1

  $ bump_version -f post -i 1 -s pep440
  $ bump_version -n -f dev -i 1 -s pep440
  Old version: 0.10.post1
  New version: 0.10.post1.dev1

The version scheme is by default automatically determined from current version (just *simple*
versions though)::

  $ echo "1.0" > version.txt
  $ bump_version -n
  Old version: 1.0
  New version: 1.1

  $ echo "1.0.0" > version.txt
  $ bump_version -n
  Old version: 1.0.0
  New version: 1.0.1

  $ echo "1.0.0.0" > version.txt
  $ bump_version -n
  Old version: 1.0.0.0
  New version: 1.0.0.1

The current version may not exist yet, but obviously you must specify the right schema::

  $ rm -f version.txt
  $ bump_version -n -s simple2
  Old version: 0.0
  New version: 0.1

  $ bump_version -s simple3
  $ cat version.txt
  0.0.1
