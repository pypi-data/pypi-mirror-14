# -*- coding: utf-8 -*-
"""Unit-test of module 'backend' in 'msbackup' package."""

import os
import filecmp
import shutil
import subprocess
import tempfile
import unittest

from msbackup.backend import File
from test.mock import TextFile


try:
    import configparser
except ImportError:
    from six.moves import configparser

try:
    xrange
except NameError:
    xrange = range


TEST_ROOT = os.path.abspath(os.path.dirname(__file__))


class BackendFile(unittest.TestCase):
    """Test case of module 'backend' of 'msbackup' package."""

    @classmethod
    def setUpClass(cls):
        "Setting up class fixture before running tests in the class."
        config = configparser.RawConfigParser()
        config.read(os.path.join(TEST_ROOT, 'test.config'))
        cls.out = TextFile()
        cls.err = TextFile()
        cls.backend = File(config, out=cls.out, err=cls.err)

    def setUp(self):
        """Setting up the test case."""
        self.test_dir = tempfile.mkdtemp('_msbackup-test_backend')
        fout, self.test_file = tempfile.mkstemp(dir=self.test_dir)
        os.write(fout, os.urandom(16*1024))
        os.close(fout)

    def tearDown(self):
        """Tear down the test case."""
        self.out.data = u''
        self.err.data = u''
        shutil.rmtree(self.test_dir, True)

    def check(self):
        """Check results of executing back-end method."""
        archive_path = u'{}.tar.bz2'.format(self.test_file)
        self.assertTrue(os.path.exists(archive_path))
        origin = u'{}.origin'.format(self.test_file)
        os.rename(self.test_file, origin)
        params = [u'/bin/tar', u'-xjf', archive_path,
                  u'-C', os.path.dirname(archive_path)]
        with open(os.devnull, 'w') as out:
            self.assertEqual(0, subprocess.call(params, stdout=out))
        self.assertTrue(os.path.exists(self.test_file))
        self.assertTrue(filecmp.cmp(origin, self.test_file, shallow=False))

    def test_archive(self):
        """Test of method backend.File.archive()."""
        output = u'{}.tar.bz2'.format(self.test_file)
        src = os.path.basename(self.test_file)
        base_dir = os.path.dirname(output)
        self.assertEqual(0, self.backend.archive(src, output, base_dir))
        self.check()
        self.assertEqual(u'', self.out.data)
        self.assertEqual(u'', self.err.data)

    def test_backup(self):
        """Test of method backend.File.backup()."""
        self.assertEqual(0, self.backend.backup(self.test_file,
                                                self.test_dir))
        self.check()
        self.assertEqual(u'', self.out.data)
        self.assertEqual(u'', self.err.data)

    def test_backup_verbose(self):
        """Test of method backend.File.backup() with verbose output."""
        self.assertEqual(0, self.backend.backup(self.test_file,
                                                self.test_dir,
                                                verbose=True))
        self.check()
        self.assertEqual(u'Backup of {}\n'.format(self.test_file),
                         self.out.data)
        self.assertEqual(u'', self.err.data)


if __name__ == "__main__":
    import xmlrunner
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
