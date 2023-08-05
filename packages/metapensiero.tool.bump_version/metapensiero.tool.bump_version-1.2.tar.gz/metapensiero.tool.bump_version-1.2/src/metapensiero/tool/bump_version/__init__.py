# -*- coding: utf-8 -*-
# :Project:   metapensiero.tool.bump_version -- Simple tool to bump a version number
# :Created:   mer 28 nov 2012 16:28:06 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: Copyright (C) 2015, 2016 Lele Gaifax
#

import functools
import operator
import sys

from versio.version import Version
from versio.version_scheme import (
    Pep440VersionScheme,
    Simple3VersionScheme,
    Simple4VersionScheme,
    VersionScheme,
    )


Simple2VersionScheme = VersionScheme(name="A.B",
                                     parse_regex=r"^(\d+)\.(\d+)$",
                                     clear_value='0',
                                     format_str="{0}.{1}",
                                     fields=['Major', 'Minor'],
                                     description='Simple Major.Minor version scheme')

schemesmap = {
    'pep440': Pep440VersionScheme,
    'simple2': Simple2VersionScheme,
    'simple3': Simple3VersionScheme,
    'simple4': Simple4VersionScheme,
}

defaultfield = {
    Pep440VersionScheme: 'release',
    Simple2VersionScheme: 'minor',
    Simple3VersionScheme: 'tiny',
    Simple4VersionScheme: 'tiny2',
}

initialversion = {
    Pep440VersionScheme: '0.0',
    Simple2VersionScheme: '0.0',
    Simple3VersionScheme: '0.0.0',
    Simple4VersionScheme: '0.0.0.0',
}


allfields = sorted(functools.reduce(operator.or_, (set(s.fields)
                                                   for s in schemesmap.values())))


def read_version(version_txt, scheme_name):
    try:
        with open(version_txt) as f:
            version = f.read().strip()
    except IOError:
        if scheme_name == 'auto':
            print("ERROR: cannot read current version from “%s”" % version_txt)
            sys.exit(128)
        else:
            version = initialversion[schemesmap[scheme_name]]

    if scheme_name == 'auto':
        papabile = [i for i in schemesmap.items()
                    if i[0] != 'pep440' and i[1]._is_match(version)]
        if len(papabile) == 1:
            scheme = papabile[0][1]
        else:
            if len(papabile) > 1:
                print("ERROR: cannot unambiguosly determine scheme for"
                      " version “%s” (the following match: %s)" %
                      (version, ', '.join(i[0] for i in sorted(papabile))))
            else:
                print("ERROR: no scheme matches version “%s”" % version)
            sys.exit(128)
    else:
        scheme = schemesmap[scheme_name]

    try:
        return Version(version, scheme=scheme)
    except:
        print("ERROR: cannot parse “%s” with scheme %s" % (version, scheme.name))
        sys.exit(128)


try:
    from textwrap import indent
except ImportError:
    # For Python 2.x, taken from 3.4's textwrap.py

    def indent(text, prefix, predicate=None):
        """Adds 'prefix' to the beginning of selected lines in 'text'.

        If 'predicate' is provided, 'prefix' will only be added to the lines
        where 'predicate(line)' is True. If 'predicate' is not provided,
        it will default to adding 'prefix' to all non-empty lines that do not
        consist solely of whitespace characters.
        """
        if predicate is None:
            def predicate(line):
                return line.strip()

        def prefixed_lines():
            for line in text.splitlines(True):
                yield (prefix + line if predicate(line) else line)
        return ''.join(prefixed_lines())


def main():
    import argparse

    version_txt = 'version.txt'

    parser = argparse.ArgumentParser(
        description="Version bumper.",
        epilog='\n\n'.join('%s:\n%s' % (name, indent(schemesmap[name].description, '  '))
                           for name in sorted(schemesmap)),
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('file', default=version_txt, nargs='?',
                        help="The file containing the version number, by default"
                        " “%s”" % version_txt)
    parser.add_argument('-s', '--scheme', default='auto',
                        choices=['auto'] + sorted(schemesmap.keys()),
                        help="Scheme to follow, by default “auto” that tries to figure"
                        " out the right (simple) scheme from the current version")
    parser.add_argument('-f', '--field', choices=['auto'] + allfields, default='auto',
                        help="Which field to bump, by default the least significative number")
    parser.add_argument('-i', '--index', default=-1, type=int,
                        help="For scheme pep440, the part of the release number"
                        " to bump")
    parser.add_argument('-n', '--dry-run', default=False, action="store_true",
                        help="Do not rewrite the file, just print the new version")

    args = parser.parse_args()

    version = read_version(args.file, args.scheme)

    if args.field == 'auto':
        args.field = defaultfield[version.scheme]

    if not args.field in version.scheme.fields:
        print("ERROR: field “%s” not recognized by scheme %s"
              " (hint: choose one between %s)" %
              (args.field, version.scheme.name, version.scheme.fields))
        sys.exit(128)

    if args.dry_run:
        print("Old version: %s" % version)

    version.bump(args.field, args.index)

    if args.dry_run:
        print("New version: %s" % version)
    else:
        with open(args.file, 'w') as s:
            s.write(str(version))


if __name__ == '__main__':
    main()
