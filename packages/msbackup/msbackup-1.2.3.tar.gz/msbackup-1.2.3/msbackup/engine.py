# -*- coding: utf-8 -*-
"""Backup engine class definition module."""

import calendar
from datetime import date, timedelta
import os
import re
import shutil
import sys

from dateutil.relativedelta import relativedelta
import getpass

try:
    from msbackup.backend import make_backend
except ImportError:
    from .backend import make_backend


class Engine(object):
    """Backup engine class."""

    DATE_FORMAT = '%Y-%m-%d'
    COMMON = '^(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})'
    DEFAULT_OPTIONS = {'MONTH_SUFFIX': '-monthly',
                       'WEEK_SUFFIX': '-weekly',
                       'DAY_SUFFIX': '-daily'}

    def __init__(self, backend, config,
                 archiver=None, encryptor=None,
                 out=None, err=None, **kwargs):
        """
        Backup engine constructor.

        :param backend: Backend identifier.
        :param backend: str
        :param config: Config object.
        :type config: :class:`ConfigParser.RawConfigParser`
        :param archiver: Name of file archiver.
        :type archiver: basestring
        :param encryptor: Name of file encryptor.
        :type encryptor: basestring
        :param out: Stream to messages output.
        :param err: Stream to errors output.
        """
        self.backend = make_backend(backend, config,
                                    archiver=archiver,
                                    encryptor=encryptor,
                                    out=out,
                                    err=err)
        # -- Load configuration --
        SECTION = self.backend.SECTION
        # backup_user
        backup_user = None
        if config.has_option(SECTION, 'BACKUP_USER'):
            backup_user = config.get(SECTION, 'BACKUP_USER').strip()
        elif config.has_option('DEFAULT', 'BACKUP_USER'):
            backup_user = config.get('DEFAULT', 'BACKUP_USER').strip()
        if backup_user is not None and len(backup_user) > 0:
            if getpass.getuser() != backup_user:
                raise Exception(u'This program must be run as {}. '
                                u'Exiting.'.format(backup_user))
        # source
        if config.has_option(SECTION, 'SOURCE'):
            self.source = config.get(SECTION, 'SOURCE')
        elif config.has_option('DEFAULT', 'SOURCE'):
            self.source = config.get('DEFAULT', 'SOURCE')
        else:
            self.source = None
        # backup_dir
        if config.has_option(SECTION, 'BACKUP_DIR'):
            self.backup_dir = config.get(SECTION, 'BACKUP_DIR')
        elif config.has_option('DEFAULT', 'BACKUP_DIR'):
            self.backup_dir = config.get('DEFAULT', 'BACKUP_DIR')
        else:
            self.backup_dir = None
        # day_month_keep
        if config.has_option(SECTION, 'DAY_OF_MONTH_TO_KEEP'):
            self.day_month_keep = config.getint(SECTION, 'DAY_OF_MONTH_TO_KEEP')
        elif config.has_option('DEFAULT', 'DAY_OF_MONTH_TO_KEEP'):
            self.day_month_keep = config.getint('DEFAULT', 'DAY_OF_MONTH_TO_KEEP')
        else:
            self.day_month_keep = 1
        # months_keep
        if config.has_option(SECTION, 'MONTHS_TO_KEEP'):
            self.months_keep = config.getint(SECTION, 'MONTHS_TO_KEEP')
        elif config.has_option('DEFAULT', 'MONTHS_TO_KEEP'):
            self.months_keep = config.getint('DEFAULT', 'MONTHS_TO_KEEP')
        else:
            self.months_keep = 1
        # day_week_keep
        if config.has_option(SECTION, 'DAY_OF_WEEK_TO_KEEP'):
            self.day_week_keep = config.getint(SECTION, 'DAY_OF_WEEK_TO_KEEP')
        elif config.has_option('DEFAULT', 'DAY_OF_WEEK_TO_KEEP'):
            self.day_week_keep = config.getint('DEFAULT', 'DAY_OF_WEEK_TO_KEEP')
        else:
            self.day_week_keep = 1
        # weeks_keep
        if config.has_option(SECTION, 'WEEKS_TO_KEEP'):
            self.weeks_keep = config.getint(SECTION, 'WEEKS_TO_KEEP')
        elif config.has_option('DEFAULT', 'WEEKS_TO_KEEP'):
            self.weeks_keep = config.getint('DEFAULT', 'WEEKS_TO_KEEP')
        else:
            self.weeks_keep = 4
        # days_keep
        if config.has_option(SECTION, 'DAYS_TO_KEEP'):
            self.days_keep = config.getint(SECTION, 'DAYS_TO_KEEP')
        elif config.has_option('DEFAULT', 'DAYS_TO_KEEP'):
            self.days_keep = config.getint('DEFAULT', 'DAYS_TO_KEEP')
        else:
            self.days_keep = 7
        # -- Options
        options = self.DEFAULT_OPTIONS.copy()
        if kwargs:
            options.update(kwargs)
        self.month_suffix = options['MONTH_SUFFIX']
        self.week_suffix = options['WEEK_SUFFIX']
        self.day_suffix = options['DAY_SUFFIX']
        self.re_month = re.compile(self.COMMON + self.month_suffix)
        self.re_week = re.compile(self.COMMON + self.week_suffix)
        self.re_day = re.compile(self.COMMON + self.day_suffix)

    def out(self, data):
        """Output data to standard stream."""
        self.backend.out(data)

    def err(self, data):
        """Output data to error stream."""
        self.backend.err(data)

    def backup(self, source=None, backup_dir=None, verbose=False, suffix=u''):
        """
        Perform backup of source into archive directory.

        :param source: Path to source of backup.
        :type source: basestring
        :param backup_dir: Path to directory for store archives.
        :type backup_dir: basestring
        :param verbose: Print verbose messages.
        :type verbose: bool
        :param suffix: Archives directory name suffix.
        :type suffix: basestring
        :param out: Output stream.
        :type out: Object with write() method.
        :param err: Error stream.
        :type err: Object with write() method.
        :return: Path to archive directory.
        :rtype: basestring
        """
        if verbose:
            self.out(u'Backup started.\n----------------------\n')
        if source is None:
            source = self.source
        if backup_dir is None:
            backup_dir = self.backup_dir
        if not os.path.exists(backup_dir):
            os.mkdir(backup_dir)
        archive_name = date.today().strftime(self.DATE_FORMAT) + suffix
        archive_dir = os.path.join(backup_dir, archive_name)
        if not os.path.exists(archive_dir):
            if verbose:
                self.out(u'Making archive directory in {}\n'
                         .format(archive_dir))
            try:
                os.mkdir(archive_dir)
            except:
                sys.stderr.write(u'Cannot create archive directory in {}. '
                                 u'Go and fix it!\n'.format(archive_dir))
                raise
        if verbose:
            self.out(u'\nPerforming backups\n----------------------\n')
        ec = self.backend.backup(source, archive_dir, verbose)
        if verbose:
            self.out(u'----------------------\nAll backups complete!\n')
            if ec != 0:
                self.err(u'')
        return archive_dir

    def _remove_expired(self, backup_dir, expire, regexp):
        """
        Remove expired archives based on configuration.

        :param backup_dir: Path to archives directory.
        :type backup_dir: basestring
        :param expire: Datetime of oldest archive to keep.
        :type expire: datetime
        :param regexp: Regular expression to match archive directory.
        :type regexp: regexp
        """
        if not os.path.exists(backup_dir) or not os.path.isdir(backup_dir):
            return
        for entry in os.listdir(backup_dir):
            arch_path = os.path.join(backup_dir, entry)
            if not os.path.isdir(arch_path):
                continue
            m = regexp.match(entry)
            if not m:
                continue
            entry_date = date(int(m.group('year')),
                              int(m.group('month')),
                              int(m.group('day')))
            if entry_date <= expire:
                shutil.rmtree(arch_path, True)

    def rotated(self, source=None, backup_dir=None, verbose=False):
        """
        Perform rotated archive with removing expired archives.

        :param source: Path to source directory.
        :type source: basestring
        :param backup_dir: Path to archives directory.
        :type backup_dir: basestring
        :param verbose: Print verbosity messages.
        :type verbose: bool
        """
        if source is None:
            source = self.source
        if backup_dir is None:
            backup_dir = self.backup_dir
        today = date.today()
        # Monthly backup.
        days_in_month = calendar.monthrange(today.year, today.month)[1]
        day_month_keep = min(self.day_month_keep, days_in_month)
        if today.day == day_month_keep:
            # Delete expired monthly backups.
            expire = today - relativedelta(months=self.months_keep)
            self._remove_expired(backup_dir, expire, self.re_month)
            return self.backup(source, backup_dir, verbose, self.month_suffix)
        # Weekly backup.
        if today.isoweekday() == self.day_week_keep:
            expire = today - timedelta(weeks=self.weeks_keep)
            self._remove_expired(backup_dir, expire, self.re_week)
            return self.backup(source, backup_dir, verbose, self.week_suffix)
        # Daily backup.
        expire = today - timedelta(days=self.days_keep)
        self._remove_expired(backup_dir, expire, self.re_day)
        return self.backup(source, backup_dir, verbose, self.day_suffix)
