# -*- coding: utf-8 -*-
"""Encryption module."""

import os
import subprocess


class Gpg(object):
    """GnuPG encryptor class."""

    SECTION = 'Encrypt-GnuPG'

    def __init__(self, config):
        """
        Class constructor.

        :param config: Config object.
        :type config: :class:`ConfigParser.RawConfigParser`
        """
        if config.has_option(self.SECTION, 'COMMAND'):
            self.cmd = config.get(self.SECTION, 'COMMAND')
        else:
            self.cmd = '/usr/bin/gpg'
        if config.has_option(self.SECTION, 'RECIPIENT'):
            self.recipient = config.get(self.SECTION, 'RECIPIENT')
        else:
            self.recipient = None
        if config.has_option(self.SECTION, 'SUFFIX'):
            self.suffix = config.get(self.SECTION, 'SUFFIX')
        else:
            self.suffix = '.gpg'

    def encrypt(self, source, output=None):
        """
        Encrypt file.

        :param source: Path to file to encrypt.
        :type source: basestring
        :param output: Path to output encrypted file.
        :type output: basestring
        """
        params = [self.cmd, '--quiet']
        if output is None:
            output = source + self.suffix
        params.append('--output')
        params.append(output)
        if self.recipient is not None:
            params.append('--recipient')
            params.append(self.recipient)
        else:
            params.append('--default-recipient-self')
        params.append('--encrypt')
        params.append(source)
        with open(os.devnull, 'w') as out:
            return subprocess.call(params, stderr=out)


ENCRYPTORS = {'gpg': Gpg}


def make_encryptor(name, config):
    """
    Create encryptor object.

    :param name: Name of encryptor to create.
    :type name: basestring
    :param config: Config object.
    :type config: :class:`ConfigParser.RawConfigParser`
    """
    if name not in ENCRYPTORS:
        raise Exception(u'Unknown encryptor: {}'.format(name))
    return ENCRYPTORS[name](config)
