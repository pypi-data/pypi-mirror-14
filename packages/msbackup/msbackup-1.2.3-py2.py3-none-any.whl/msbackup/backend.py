# -*- coding: utf-8 -*-
"""Backends for 'msbackup' package."""

import os
import shutil
import subprocess
import sys
import tempfile


try:
    from msbackup.archive import make_archiver
except ImportError:
    from .archive import make_archiver

try:
    from msbackup.encrypt import make_encryptor
except ImportError:
    from .encrypt import make_encryptor


def dequote(s):
    """
    If a string has single or double quotes around it, remove them.

    Make sure the pair of quotes match.
    If a matching pair of quotes is not found, return the string unchanged.
    """
    if (s[0] == s[-1]) and s.startswith(("'", '"')):
        return s[1:-1]
    return s


class Base(object):
    """Base back-end."""

    SECTION = 'DEFAULT'

    def __init__(self, config, archiver=None, encryptor=None,
                 out=None, err=None):
        """
        Constructor.

        :param config: Config object.
        :type config: :class:`ConfigParser.RawConfigParser`
        :param archiver: Name of file archiver.
        :type archiver: basestring
        :param encryptor: Name of file encryptor.
        :type encryptor: basestring
        :param out: Output stream.
        :param err: Output stream of error messages.
        """
        self.stream_out = sys.stdout if out is None else out
        self.stream_err = sys.stderr if err is None else err
        # Encryptor
        encryptor_name = None
        if encryptor is not None:
            encryptor_name = encryptor
        elif config.has_option(self.SECTION, 'ENCRYPTOR'):
            encryptor_name = config.get(self.SECTION, 'ENCRYPTOR')
        if encryptor_name is not None:
            self.encryptor = make_encryptor(encryptor_name, config)
        else:
            self.encryptor = None
        # Archiver
        archiver_name = 'tar'
        if archiver is not None:
            archiver_name = archiver
        elif config.has_option(self.SECTION, 'ARCHIVER'):
            archiver_name = config.get(self.SECTION, 'ARCHIVER')
        self.archiver = make_archiver(archiver_name, config, self.encryptor)

    def outpath(self, archive_dir, name):  # pragma: no cover
        """
        Generate archive file name.

        :param archive_dir: Path to archive directory.
        :type archive_dir: basestring
        :param name: Name of archive file without extensions.
        :type name: basestring
        :return: Full path to archive file.
        :rtype: basestring
        """
        fname = name + self.archiver.suffix
        return os.path.join(archive_dir, fname)

    def archive(self, source, output, base_dir=None):  # pragma: no cover
        """
        Archive object.

        :param source: Source identifier.
        :type source: basestring
        :param output: Path to archive file.
        :type output: basestring
        :param base_dir: Path to base directory of source.
        :type base_dir: basestring
        :return: Exit code.
        :rtype: int
        """
        raise NotImplementedError()

    def backup(self, source, archive_dir, verbose=False):  # pragma: no cover
        """
        Backup object.

        :param source: Source identifier.
        :type source: basestring
        :param archive_dir: Path to archive directory.
        :type archive_dir: basestring
        :param verbose: Print verbose messages.
        :type verbose: bool
        """
        raise NotImplementedError()

    def out(self, data):
        """Output data to standard stream."""
        self.stream_out.write(data)

    def err(self, data):
        """Output data to error stream."""
        self.stream_err.write(data)


class File(Base):
    """File backend."""

    SECTION = 'Backend-File'

    def __init__(self, config, archiver=None, encryptor=None,
                 out=None, err=None):
        """
        Constructor.

        :param config: Config object.
        :type config: :class:`ConfigParser.RawConfigParser`
        :param out: Output stream.
        :param err: Output stream of error messages.
        :param encryptor: Name of file encryptor.
        :type encryptor: basestring
        """
        super(File, self).__init__(config,
                                   archiver=archiver,
                                   encryptor=encryptor,
                                   out=out,
                                   err=err)

    def archive(self, source, output, base_dir=None):
        """
        Archive filesystem object.

        :param source: Path to source file or directory.
        :type source: basestring
        :param output: Path to archive file.
        :type output: basestring
        :param base_dir: Path to base directory of source.
        :type base_dir: basestring
        :return: Exit code.
        :rtype: int
        """
        return self.archiver.pack(source, output, base_dir)


    def backup(self, source, archive_dir, verbose=False):
        """
        Backup file or directory in filesystem.

        :param source: Path to source in filesystem.
        :type source: basestring
        :param archive_dir: Path to archive directory.
        :type archive_dir: basestring
        :param base_dir: Path to base directory of source.
        :type base_dir: basestring
        :param verbose: Print verbose messages.
        :type verbose: bool
        """
        if verbose:
            self.out(u'Backup of {}\n'.format(source))
        output = self.outpath(archive_dir, os.path.basename(source))
        base_dir = None
        if os.path.isfile(source):
            stype = u'file'
            base_dir = os.path.dirname(source)
            source = os.path.basename(source)
        else:
            stype = u'directory'
        ec = self.archive(source, output, base_dir)
        if ec != 0:
            self.err(u'[ERROR!] Failed archive {}: {}\n'.format(stype, source))
        return ec


class Subversion(Base):
    """Subversion backend."""

    SECTION = 'Backend-Subversion'

    def __init__(self, config, archiver=None, encryptor=None,
                 out=None, err=None):
        """
        Constructor.

        :param config: Config object.
        :type config: :class:`ConfigParser.RawConfigParser`
        :param out: Output stream.
        :param err: Output stream of error messages.
        :param encryptor: Name of file encryptor.
        :type encryptor: basestring
        """
        super(Subversion, self).__init__(config,
                                         archiver=archiver,
                                         encryptor=encryptor,
                                         out=out,
                                         err=err)

    def outpath(self, archive_dir, name):
        """
        Generate archive file name.

        :param archive_dir: Path to archive directory.
        :type archive_dir: basestring
        :param name: Name of archive file without extensions.
        :type name: basestring
        :return: Full path to archive file.
        :rtype: basestring
        """
        retvalue = os.path.join(archive_dir, u'{}.svn.bz2'.format(name))
        return retvalue

    def archive(self, source, output):
        """
        Archive Subversion repository.

        :param source: Path to source repository.
        :type source: basestring
        :param output: Path to archive file.
        :type output: basestring
        :return: Exit code.
        :rtype: int
        """
        name = os.path.basename(source)
        repo_copy_dir = tempfile.mkdtemp()
        repo_copy = os.path.join(repo_copy_dir, name)
        with open(os.devnull, 'wb') as out:
            ec = subprocess.call(['/usr/bin/svnadmin', 'hotcopy',
                                  '--clean-logs', source, repo_copy],
                                 stdout=out)
        if ec != 0 :
            return ec
        tmp_path = output + '.tmp'
        p1 = subprocess.Popen(['/usr/bin/svnadmin', 'dump', '--quiet',
                              '--deltas', repo_copy],
                              stdout=subprocess.PIPE)
        with open(tmp_path, 'wb') as out:
            p2 = subprocess.Popen(['/bin/bzip2', '-q9'],
                                  stdin=p1.stdout,
                                  stdout=out)
        p1.stdout.close()
        ec = p2.wait()
        shutil.rmtree(repo_copy_dir, True)
        if ec != 0 :
            return ec
        if self.encryptor is not None:
            output += self.encryptor.suffix
            ec = self.encryptor.encrypt(tmp_path, output)
            os.remove(tmp_path)
        else:
            shutil.move(tmp_path, output)
        os.chmod(output, self.archiver.ARCHIVE_PERMISSIONS)
        return ec

    def backup(self, repos_dir, archive_dir, verbose=False):
        """
        Backup of all Subversion repositories in repos directory.

        :param repos_dir: Path to repos directory.
        :type repos_dir: basestring
        :param archive_dir: Path to archive directory.
        :type archive_dir: basestring
        :param verbose: Print verbose messages.
        :type verbose: bool
        :return: Exit code.
        :rtype: int
        """
        retvalue = 0
        for source in os.listdir(repos_dir):
            repo_path = os.path.join(repos_dir, source)
            if not os.path.isdir(repo_path):
                continue
            svnfmt = os.path.join(repo_path, 'format')
            if not (os.path.exists(svnfmt) and os.path.isfile(svnfmt)):
                continue
            if verbose:
                self.out(u'Backup of {}\n'.format(source))
            output = self.outpath(archive_dir, source)
            ec = self.archive(repo_path, output)
            if ec != 0:
                self.err(u'[ERROR!] Failed archive repo: {}\n'.format(source))
                if ec > retvalue:
                    retvalue = ec
        return retvalue


class Mercurial(Base):
    """Mercurial backend."""

    SECTION = 'Backend-Mercurial'

    def __init__(self, config, archiver=None, encryptor=None,
                 out=None, err=None):
        """
        Constructor.

        :param config: Config object.
        :type config: :class:`ConfigParser.RawConfigParser`
        :param out: Output stream.
        :param err: Output stream of error messages.
        :param encryptor: Name of file encryptor.
        :type encryptor: basestring
        """
        super(Mercurial, self).__init__(config,
                                        archiver=archiver,
                                        encryptor=encryptor,
                                        out=out,
                                        err=err)

    def archive(self, source, output):
        """
        Archive Mercurial repository.

        :param source: Path to source repository.
        :type source: basestring
        :param output: Path to archive file.
        :type output: basestring
        :return: Exit code.
        :rtype: int
        """
        name = os.path.basename(source)
        repo_bak_dir = tempfile.mkdtemp()
        repo_bak = os.path.join(repo_bak_dir, name)
        with open(os.devnull, 'w') as out:
            ec = subprocess.call(['/usr/bin/hg', 'clone', '--noupdate',
                                  '--quiet', source, repo_bak],
                                 stderr=out)
        if ec != 0:
            return ec
        ec = self.archiver.pack(name, output, repo_bak_dir)
        shutil.rmtree(repo_bak_dir, True)
        return ec

    def backup(self, repos_dir, archive_dir, verbose=False):
        """
        Backup of all Mercurial repositories in repos directory.

        :param repos_dir: Path to repos directory.
        :type repos_dir: basestring
        :param archive_dir: Path to archive directory.
        :type archive_dir: basestring
        :param verbose: Print verbose messages.
        :type verbose: bool
        :return: Exit code.
        :rtype: int
        """
        retvalue = 0
        for source in os.listdir(repos_dir):
            repo_path = os.path.join(repos_dir, source)
            if not os.path.isdir(repo_path):
                continue
            hgdir = os.path.join(repo_path, '.hg')
            if not (os.path.exists(hgdir) and os.path.isdir(hgdir)):
                continue
            if verbose:
                self.out(u'Backup of {}\n'.format(source))
            output = self.outpath(archive_dir, os.path.basename(repo_path))
            ec = self.archive(repo_path, output)
            if ec != 0:
                self.out(u'[ERROR!] Failed archive repo: {}\n'.format(source))
                if ec > retvalue:
                    retvalue = ec
        return retvalue


class PostgreSQL(Base):
    """PostgreSQL backend."""

    SECTION = 'Backend-PostgreSQL'

    FORMAT_NONE = 0  # Формат архива не задан.
    FORMAT_PLAIN = 1  # Полный архив БД в текстовом формате.
    FORMAT_CUSTOM = 2  # Полный архив БД в сжатом формате.

    FORMAT_MAP = {'plain': FORMAT_PLAIN,
                  'custom': FORMAT_CUSTOM}

    MODE_NONE = 0  # Запрет архивирования БД.
    MODE_SCHEMA = 1  # Архивировать только схему БД.
    MODE_FULL = 2  # Полный архив БД.

    def __init__(self, config, archiver=None, encryptor=None,
                 out=None, err=None):
        """
        Constructor.

        :param config: Config object.
        :type config: :class:`ConfigParser.RawConfigParser`
        :param out: Output stream.
        :param err: Output stream of error messages.
        :param encryptor: Name of file encryptor.
        :type encryptor: basestring
        """
        super(PostgreSQL, self).__init__(config,
                                         archiver=archiver,
                                         encryptor=encryptor,
                                         out=out,
                                         err=err)
        # hostname
        self.hostname = None
        if config.has_option(self.SECTION, 'HOSTNAME'):
            hostname = config.get(self.SECTION, 'HOSTNAME').strip()
            if len(hostname) > 0:
                self.hostname = hostname
        # port
        self.port = None
        if config.has_option(self.SECTION, 'PORT'):
            port = config.get(self.SECTION, 'PORT').strip()
            if len(port) > 0:
                self.port = port
        # username
        if config.has_option(self.SECTION, 'USERNAME'):
            username = config.get(self.SECTION, 'USERNAME').strip()
        else:
            username = ''
        if len(username) > 0:
            self.username = username
        else:
            self.username = u'postgres'
        # format
        self.format = self.FORMAT_NONE
        if config.has_option(self.SECTION, 'BACKUP_FORMAT'):
            format_name = config.get(self.SECTION, 'BACKUP_FORMAT')
            if format_name in self.FORMAT_MAP:
                self.format = self.FORMAT_MAP[format_name]
        # schema_only_list
        self.schema_only_list = []
        if config.has_option(self.SECTION, 'SCHEMA_ONLY_LIST'):
            lst = dequote(config.get(self.SECTION, 'SCHEMA_ONLY_LIST'))
            self.schema_only_list.extend(lst.split(' '))
        # psql_cmd
        if config.has_option(self.SECTION, 'PSQL_COMMAND'):
            self.psql_cmd = config.get(self.SECTION, 'PSQL_COMMAND')
        else:
            self.psql_cmd = u'/usr/bin/psql'
        # pgdump_cmd
        if config.has_option(self.SECTION, 'PGDUMP_COMMAND'):
            self.pgdump_cmd = config.get(self.SECTION, 'PGDUMP_COMMAND')
        else:
            self.pgdump_cmd = u'/usr/bin/pg_dump'

    def outpath(self, archive_dir, name, mode=MODE_NONE):
        """
        Generate archive file name.

        :param archive_dir: Path to archive directory.
        :type archive_dir: basestring
        :param name: Name of archive file without extensions.
        :type name: basestring
        :return: Full path to archive file.
        :rtype: basestring
        """
        fname = name
        if mode == self.MODE_SCHEMA:
            fname += u'_SCHEMA.sql.gz'
        elif self.format == self.FORMAT_PLAIN:
            fname += u'.sql.gz'
        elif self.format == self.FORMAT_CUSTOM:
            fname += u'.custom'
        return os.path.join(archive_dir, fname)

    def archive(self, source, output, mode=MODE_NONE):
        """
        Archive PostgreSQL database.

        :param source: Database name.
        :type source: basestring
        :param output: Path to archive file.
        :type output: basestring
        :param base_dir: Path to base directory of source (ignored).
        :type base_dir: basestring
        :return: Exit code.
        :rtype: int
        """
        tmp_path = output + self.archiver.progress_suffix
        if self.format == self.FORMAT_CUSTOM:
            proc = self.dump_proc(source, tmp_path, mode)
        else:
            p1 = self.dump_proc(source, tmp_path, mode, stdout=subprocess.PIPE)
            with open(tmp_path, 'wb') as out:
                proc = subprocess.Popen([u'/bin/gzip', u'-q9'],
                                        stdin=p1.stdout, stdout=out)
            p1.stdout.close()
        ec = proc.wait()
        if ec != 0 :
            return ec
        if self.encryptor is not None:
            output += self.encryptor.suffix
            ec = self.encryptor.encrypt(tmp_path, output)
            os.remove(tmp_path)
        else:
            shutil.move(tmp_path, output)
        return ec


    def backup(self, source, archive_dir, verbose=False):
        """
        Backup PostgreSQL databases.

        :param source: Database server host or socket directory.
        :type source: basestring
        :param archive_dir: Path to archive directory.
        :type archive_dir: basestring
        :param base_dir: Path to base directory of source (ignored).
        :type base_dir: basestring
        :param verbose: Print verbose messages.
        :type verbose: bool
        """
        dblist = [source] if source is not None else self.dblist()
        for database in dblist:
            mode = (self.MODE_SCHEMA if database in self.schema_only_list
                    else self.MODE_FULL)
            if verbose:
                info = u''
                if mode == self.MODE_SCHEMA:
                    info = u'Schema-only'
                elif self.format == self.FORMAT_PLAIN:
                    info = u'Plain'
                elif self.format == self.FORMAT_CUSTOM:
                    info = u'Custom'
                else:
                    info = u'Default'
                self.out(u'{} backup of {}\n'.format(info, database))
            ec = self.archive(database,
                              self.outpath(archive_dir, database, mode),
                              mode)
            if ec != 0:
                self.err(u'[ERROR!] Failed backup database: {}\n'
                         .format(database))
        return ec

    def dblist(self):
        """
        Database list on the target host.

        :return: List of all databases.
        :rtype: list
        """
        params = [self.psql_cmd]
        if self.hostname is not None:
            params.append(u'--hostname={}'.format(self.hostname))
        if self.port is not None:
            params.append(u'--port={}'.format(self.port))
        params.append(u'--username={}'.format(self.username))
        params.append(u'--no-align')
        params.append(u'--tuples-only')
        params.append(u'-c')
        params.append(u'SELECT datname '
                      u'FROM pg_database '
                      u'WHERE NOT datistemplate '
                      u'ORDER BY datname;')
        params.append(u'postgres')
        out = subprocess.check_output(params)
        return out.decode(sys.getdefaultencoding()).splitlines()

    def dump_proc(self, database, output, mode, **kwargs):
        """
        Create process of dump PostgreSQL database.

        :param database: Database name.
        :type database: basestring
        :param output: Path to archive file.
        :type output: basestring
        :param mode: Database backup mode.
        :type mode: int
        :param **kwargs: Arguments of `subprocess.Popen()` constructor.
        :type **kwargs: dict
        """
        params = [self.pgdump_cmd]
        if mode == self.MODE_SCHEMA or self.format == self.FORMAT_PLAIN:
            params.append(u'--format=p')
        elif self.format == self.FORMAT_CUSTOM:
            params.append(u'--format=c')
        if mode == self.MODE_SCHEMA:
            params.append(u'--schema-only')
        if self.hostname is not None:
            params.append(u'--hostname={}'.format(self.hostname))
        if self.port is not None:
            params.append(u'--port={}'.format(self.port))
        params.append(u'--username={}'.format(self.username))
        params.append(u'--oids')
        if self.format == self.FORMAT_CUSTOM:
            params.append(u'--file={}'.format(output))
        params.append(database)
        return subprocess.Popen(params, **kwargs)


BACKENDS = {'file': File,
            'subversion': Subversion,
            'mercurial': Mercurial,
            'postgresql': PostgreSQL}


def make_backend(name, config, archiver=None, encryptor=None,
                 out=None, err=None):
    """
    Create back-end object.

    :param name: Name of back-end to create.
    :type name: basestring
    :param config: Config object.
    :type config: :class:`ConfigParser.RawConfigParser`
    :param archiver: Name of file archiver.
    :type encryptor: basestring
    :param encryptor: Name of file encryptor.
    :type encryptor: basestring
    :param out: Output stream.
    :param err: Output stream of error messages.
    """
    if name not in BACKENDS:
        raise Exception('Unknown back-end: {}'.format(name))
    return BACKENDS[name](config,
                          archiver=archiver,
                          encryptor=encryptor,
                          out=out,
                          err=err)
