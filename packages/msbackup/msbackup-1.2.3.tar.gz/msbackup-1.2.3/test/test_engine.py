# -*- coding: utf-8 -*-
"""Unit-test of module 'backend' in 'msbackup' package."""

import os
import shutil
import subprocess
import tempfile
import unittest

from test.mock import TextFile, MockEngine
import filecmp
from datetime import date


try:
    xrange
except NameError:
    xrange = range

try:
    import configparser
except ImportError:
    from six.moves import configparser

try:
    from msbackup.engine import Engine
except ImportError:
    from .engine import Engine


TEST_ROOT = os.path.abspath(os.path.dirname(__file__))


class TestEngineInit(unittest.TestCase):
    """Test case of method msbackup.engine.Engine.init()."""

    @classmethod
    def setUpClass(cls):
        """Setting up class fixture before running tests in the class."""
        cls.config = configparser.RawConfigParser()
        cls.config.read(os.path.join(TEST_ROOT, 'test.config'))

    def test_init_default(self):
        """Test of default init."""
        engine = Engine('file', self.config)
        self.assertEqual('Backend-File', engine.backend.SECTION)
        self.assertEqual(engine.month_suffix, '-monthly')
        self.assertEqual(engine.week_suffix, '-weekly')
        self.assertEqual(engine.day_suffix, '-daily')

    def test_init_custom(self):
        """Test of custom init."""
        options = {'MONTH_SUFFIX': u'-месяц',
                   'WEEK_SUFFIX': u'-неделя',
                   'DAY_SUFFIX': u'-день'}
        engine = Engine('mercurial', self.config, **options)
        self.assertEqual('Backend-Mercurial', engine.backend.SECTION)
        self.assertEqual(engine.month_suffix, u'-месяц')
        self.assertEqual(engine.week_suffix, u'-неделя')
        self.assertEqual(engine.day_suffix, u'-день')

    def test_init_error(self):
        """Test of init with unknown back-end."""
        with self.assertRaises(Exception) as cm:
            Engine('error', self.config)
        try:
            msg = unicode(cm.exception)
        except NameError:
            msg = str(cm.exception)
        self.assertEqual('Unknown back-end: error', msg)


class TestEngineFile(unittest.TestCase):
    """Test case of Engine with 'file' back-end."""

    @classmethod
    def setUpClass(cls):
        """Setting up class fixture before running tests in the class."""
        cls.out = TextFile()
        cls.err = TextFile()
        cls.config = configparser.RawConfigParser()
        cls.config.read(os.path.join(TEST_ROOT, 'test.config'))
        cls.engine = Engine('file', cls.config, out=cls.out, err=cls.err)
        cls.mock_engine = MockEngine('file', cls.config,
                                     out=cls.out, err=cls.err)
        cls.test_dir = tempfile.mkdtemp(suffix='_msbackup-test_engine-file')

    @classmethod
    def tearDownClass(cls):
        """Destroy the class fixture after running all tests in the class."""
        shutil.rmtree(cls.test_dir, True)

    def setUp(self):
        """Setting up the test case."""
        self.source = os.path.join(self.test_dir, 'source')
        self.backup = os.path.join(self.test_dir, 'backup')
        self.restore = os.path.join(self.test_dir, 'restore')
        os.mkdir(self.source)
        os.mkdir(self.restore)
        self.filelist = []
        for num in xrange(10):
            fout, fname = tempfile.mkstemp(prefix=u'тест-',
                                           suffix=u'.{}'.format(num),
                                           dir=self.source)
            self.filelist.append(fname)
            os.write(fout, os.urandom(16 * 1024))

    def tearDown(self):
        """Tear down the test case."""
        self.mock_engine._clear()
        self.out.data = ''
        self.err.data = ''
        shutil.rmtree(self.source, True)
        shutil.rmtree(self.backup, True)
        shutil.rmtree(self.restore, True)

    def test_backup(self):
        """Test of method Engine.backup()."""
        archive_dir = self.engine.backup(source=self.source,
                                         backup_dir=self.backup,
                                         suffix=u'-тест')
        self.assertEqual(os.path.abspath(self.backup),
                         os.path.abspath(os.path.join(archive_dir,
                                                      os.path.pardir)))
        archive = os.path.join(archive_dir, 'source.tar.bz2')
        self.assertTrue(os.path.exists(archive))
        self.assertEqual('', self.out.data)
        self.assertEqual('', self.err.data)
        args = ['/bin/tar', '-xjf', archive, '-C', self.restore]
        with open(os.devnull, 'w') as out:
            self.assertEqual(0, subprocess.call(args, stdout=out))
        rest_dir = os.path.join(self.restore, os.path.basename(self.source))
        self.assertTrue(filecmp.cmpfiles(self.source, rest_dir,
                                         self.filelist, shallow=False))

    def test_backup_verbose(self):
        """Test of method Engine.backup()."""
        archive_dir = self.engine.backup(source=self.source,
                                         backup_dir=self.backup,
                                         verbose=True,
                                         suffix=u'-тест')
        self.assertEqual(os.path.abspath(self.backup),
                         os.path.abspath(os.path.join(archive_dir,
                                                      os.path.pardir)))
        archive = os.path.join(archive_dir, 'source.tar.bz2')
        self.assertTrue(os.path.exists(archive))
        self.assertEqual(u'Backup started.\n'
                         u'----------------------\n'
                         u'Making archive directory in '
                         u'{backup}/{date}-тест\n\n'
                         u'Performing backups\n'
                         u'----------------------\n'
                         u'Backup of {source}\n'
                         u'----------------------\n'
                         u'All backups complete!\n'.format(backup=self.backup,
                                                           date=date.today(),
                                                           source=self.source),
                         self.out.data)
        self.assertEqual('', self.err.data)
        args = ['/bin/tar', '-xjf', archive, '-C', self.restore]
        with open(os.devnull, 'w') as out:
            self.assertEqual(0, subprocess.call(args, stdout=out))
        rest_dir = os.path.join(self.restore, os.path.basename(self.source))
        self.assertTrue(filecmp.cmpfiles(self.source, rest_dir,
                                         self.filelist, shallow=False))

    def test_rotated_monthly(self):
        """"Test of method Engine.rotated()."""
        today = date.today()
        dom = self.mock_engine.day_month_keep
        if today.day != dom:
            self.mock_engine.day_month_keep = today.day
        self.mock_engine.rotated(source=self.source, backup_dir=self.backup)
        self.mock_engine.day_month_keep = dom
        expected_calls = [{'suffix': '-monthly',
                           'source': self.source,
                           'backup_dir': self.backup,
                           'verbose': False}]
        self.assertEqual(expected_calls, self.mock_engine._calls)
        self.assertEqual(u'', self.out.data)
        self.assertEqual(u'', self.err.data)

    def test_rotated_weekly(self):
        """"Test of method Engine.rotated()."""
        today = date.today()
        dom = self.mock_engine.day_month_keep
        if today.day == dom:
            dom_new = dom + 1
            if dom_new > 28:
                dom_new = 1
            self.mock_engine.day_month_keep = dom_new
        dow = self.mock_engine.day_week_keep
        if today.isoweekday() != dow:
            self.mock_engine.day_week_keep = today.isoweekday()
        self.mock_engine.rotated(source=self.source, backup_dir=self.backup)
        self.mock_engine.day_month_keep = dom
        self.mock_engine.day_week_keep = dow
        expected_calls = [{'suffix': '-weekly',
                           'source': self.source,
                           'backup_dir': self.backup,
                           'verbose': False}]
        self.assertEqual(expected_calls, self.mock_engine._calls)
        self.assertEqual('', self.out.data)
        self.assertEqual('', self.err.data)

    def test_rotated_daily(self):
        """"Test of method Engine.rotated()."""
        today = date.today()
        dom = self.mock_engine.day_month_keep
        if today.day == dom:
            dom_new = dom + 1
            if dom_new > 28:
                dom_new = 1
            self.mock_engine.day_month_keep = dom_new
        dow = self.mock_engine.day_week_keep
        if today.isoweekday() == dow:
            dow_new = dow + 1
            if dow_new > 7:
                dow_new = 1
            self.mock_engine.day_week_keep = dow_new
        self.mock_engine.rotated(source=self.source, backup_dir=self.backup)
        self.mock_engine.day_month_keep = dom
        self.mock_engine.day_week_keep = dow
        expected_calls = [{'suffix': '-daily',
                           'source': self.source,
                           'backup_dir': self.backup,
                           'verbose': False}]
        self.assertEqual(expected_calls, self.mock_engine._calls)
        self.assertEqual('', self.out.data)
        self.assertEqual('', self.err.data)


if __name__ == '__main__':
    import xmlrunner
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
