#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
msbackup -- Generic archive utility.

@author:     Aleksei Badiaev <aleksei.badyaev@gmail.com>
@copyright:  2015 Aleksei Badiaev. All rights reserved.
"""

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
import os
import sys

try:
    import configparser
except ImportError:
    from six.moves import configparser

try:
    from msbackup.backend import BACKENDS
except ImportError:
    from .backend import BACKENDS

try:
    from msbackup.archive import ARCHIVERS
except ImportError:
    from .archive import ARCHIVERS

try:
    from msbackup.encrypt import ENCRYPTORS
except ImportError:
    from .encrypt import ENCRYPTORS

try:
    from msbackup.engine import Engine
except ImportError:
    from .engine import Engine


__all__ = []
__date__ = '2015-10-08'
__updated__ = '2016-02-29'

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(PROJECT_ROOT, 'VERSION')) as version_file:
    __version__ = version_file.read().rstrip()


class CLIError(Exception):
    """Exception class for fatal errors."""

    def __init__(self, msg):
        """
        Constructor.

        :param msg: Description of exception.
        :type msg: basestring
        """
        super(CLIError).__init__(type(self))
        self.msg = u'E: {}'.format(msg)

    def __str__(self):
        """
        String representation.

        :return: Description of exception.
        :rtype: str
        """
        return self.msg

    def __unicode__(self):
        """
        Unicode string representation.

        :return: Description of exception.
        :rtype: basestring
        """
        return self.msg


def main(argv=None):
    """
    Entry point in application.

    :param argv: Command line arguments.
    :type argv: dict
    :return: Exit code of application.
    :rtype: int
    """
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)
    program_name = os.path.basename(sys.argv[0])
    program_version = 'v%s' % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version,
                                                     program_build_date)
    program_shortdesc = __import__('msbackup').msbackup.__doc__.split('\n')[1]
    program_license = """%s

  Created by Aleksei Badiaev on %s.
  Copyright 2015 Aleksei Badiaev. All rights reserved.

  Distributed on an 'AS IS' basis without warranties
  or conditions of any kind, either express or implied.

USAGE
""" % (program_shortdesc, str(__date__))

    try:
        backends = sorted([item for item in BACKENDS])
        archivers = sorted([item for item in ARCHIVERS])
        encryptors = sorted([item for item in ENCRYPTORS])
        # Setup argument parser
        parser = ArgumentParser(description=program_license,
                                formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument('-c', '--config', dest='config',
                            default=os.path.join(os.path.dirname(sys.argv[0]),
                                                 u'msbackup.config'),
                            help='Path to config file.')
        parser.add_argument('-e', '--backend', dest='backend', required=True,
                            choices=backends,
                            help='Backend to make archive.')
        parser.add_argument('-s', '--source', dest='source',
                            help='Path to source directory.')
        parser.add_argument('-b', '--archive-dir', dest='backup_dir',
                            help='Path to archive directory (current by default).')
        parser.add_argument('-a', '--archiver', dest='archiver',
                            choices=archivers,
                            help='Name of file archiver.')
        parser.add_argument('-E', '--encryptor', dest='encryptor',
                            choices=encryptors,
                            help='Name of file encryptor.')
        parser.add_argument('-r', '--rotated', dest='rotated',
                            action='store_true',
                            help='Perform rotated archive.')
        parser.add_argument('-v', '--verbose', dest='verbose',
                            action='store_true', help='Verbose output.')
        parser.add_argument('-V', '--version', action='version',
                            version=program_version_message)
        # Process arguments
        params = parser.parse_args()
        config = configparser.RawConfigParser()
        config.read(params.config)
        # Perform archive.
        engine = Engine(params.backend, config,
                        archiver=params.archiver,
                        encryptor=params.encryptor)
        if params.rotated:
            archive_dir = engine.rotated(params.source,
                                         params.backup_dir,
                                         params.verbose)
        else:
            archive_dir = engine.backup(params.source,
                                        params.backup_dir,
                                        params.verbose)
        if params.verbose:
            sys.stdout.write(u'Archive directory: {}\n'.format(archive_dir))
        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception as e:
        indent = len(program_name) * ' '
        sys.stderr.write(program_name + ': ' + repr(e) + '\n')
        sys.stderr.write(indent + '  for help use --help\n')
        return 1

if __name__ == "__main__":
    sys.exit(main())
