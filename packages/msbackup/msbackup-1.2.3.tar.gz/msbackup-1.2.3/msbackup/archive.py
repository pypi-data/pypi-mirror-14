# -*- coding: utf-8 -*-
"""Archivers module."""

import os
import shutil
import stat
import subprocess


class Tar(object):
    """Tar archiver class."""

    SECTION = 'Archive-Tar'
    ARCHIVE_PERMISSIONS = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP

    def __init__(self, config, encryptor=None):
        """
        Class constructor.

        :param config: Config object.
        :type config: :class:`ConfigParser.RawConfigParser`
        """
        if config.has_option(self.SECTION, 'COMMAND'):
            self.cmd = config.get(self.SECTION, 'COMMAND')
        else:
            self.cmd = '/bin/tar'
        if config.has_option(self.SECTION, 'SUFFIX'):
            self.suffix = config.get(self.SECTION, 'SUFFIX')
        else:
            self.suffix = '.tar.bz2'
        if config.has_option(self.SECTION, 'PROGRESS_SUFFIX'):
            self.progress_suffix = config.get(self.SECTION, 'PROGRESS_SUFFIX')
        else:
            self.progress_suffix = '.in_progress'
        self.encryptor = encryptor

    def pack(self, source, output=None, base_dir=None):
        """
        Pack files into archive.

        :param source: Path to file to pack.
        :type source: basestring
        :param output: Path to output packed files archive.
        :type output: basestring
        """
        tmp_path = output + self.progress_suffix
        args = ['/bin/tar', '-cjf', tmp_path]
        if base_dir is not None:
            args.extend(['-C', base_dir])
        args.append(source)
        with open(os.devnull, 'w') as out:
            ec = subprocess.call(args, stdout=out, stderr=subprocess.STDOUT)
        if ec != 0:
            return ec
        if self.encryptor is not None:
            output += self.encryptor.suffix
            ec = self.encryptor.encrypt(tmp_path, output)
            os.remove(tmp_path)
        else:
            shutil.move(tmp_path, output)
        os.chmod(output, self.ARCHIVE_PERMISSIONS)
        return ec


ARCHIVERS = {'tar': Tar}


def make_archiver(name, config, encryptor=None):
    """
    Create archiver object.

    :param name: Name of archiver.
    :type name: basestring
    :param config: Config object.
    :type config: :class:`ConfigParser.RawConfigParser`
    :param encryptor: File encryptor object.
    """
    if name not in ARCHIVERS:
        raise Exception(u'Unknown archiver: {}'.format(name))
    return ARCHIVERS[name](config, encryptor)
