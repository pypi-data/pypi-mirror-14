# -*- coding: utf-8 -*-
"""Unit-test of module 'encrypt' in 'msbackup' package."""

import os
import filecmp
import shutil
import subprocess
import tempfile
import unittest

from msbackup.encrypt import make_encryptor


try:
    xrange
except NameError:
    xrange = range

try:
    import configparser
except ImportError:
    from six.moves import configparser


TEST_ROOT = os.path.abspath(os.path.dirname(__file__))


class TestGpg(unittest.TestCase):
    """Test case of module 'encrypt' of 'msbackup' package."""

    @classmethod
    def setUpClass(cls):
        "Setting up class fixture before running tests in the class."
        cls.config = configparser.RawConfigParser()
        cls.config.read(os.path.join(TEST_ROOT, 'test.config'))
        cls.encryptor = make_encryptor('gpg', cls.config)

    def setUp(self):
        """Setting up the test case."""
        self.test_dir = tempfile.mkdtemp('_msbackup-test_encrypt')
        fout, self.test_file = tempfile.mkstemp(dir=self.test_dir)
        os.write(fout, os.urandom(16*1024))
        os.close(fout)

    def tearDown(self):
        """Tear down the test case."""
        shutil.rmtree(self.test_dir, True)

    def test_encrypt(self):
        """Test of method msbackup.encrypt.Gpg.encrypt() ."""
        self.assertEqual(0, self.encryptor.encrypt(self.test_file))
        archive_path = self.test_file + self.encryptor.suffix
        self.assertTrue(os.path.exists(archive_path))

    def test_suffix(self):
        """Test value of member encrypt.Gpg.suffix ."""
        self.assertEqual(self.encryptor.suffix, '.gpg')


if __name__ == "__main__":
    import xmlrunner
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
