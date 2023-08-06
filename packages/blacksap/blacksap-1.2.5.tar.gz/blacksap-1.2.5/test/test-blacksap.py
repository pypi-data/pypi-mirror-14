#!/usr/bin/env python
# coding=utf-8
"""Unittests for blacksap.  This tests both the cli interface and internal functions for blacksap.
"""
from __future__ import print_function
import blacksap
import os
import shutil
import time
import unittest
import warnings
from click.testing import CliRunner

__author__ = 'Jesse Almanrode (jesse@almanrode.com)'


class TestFunctions(unittest.TestCase):

    def test_read_cfg(self):
        """ Test read_cfg method
        :return: Dictionary
        """
        result = blacksap.read_cfg()
        self.assertIsInstance(result, dict)
        pass

    def test_writecfg(self):
        """ Test write_cfg method
        :return: True
        """
        cfg = blacksap.read_cfg()
        result = blacksap.write_cfg(cfg)
        self.assertTrue(result)
        pass

    def test_ttl_expired(self):
        """ Test ttl_expired method
        :return: True and False
        """
        now = time.time()
        result = blacksap.ttl_expired(now, 600)
        self.assertFalse(result)
        now -= 610
        result = blacksap.ttl_expired(now, 600)
        self.assertTrue(result)
        pass

    def test_get_torrent_file(self):
        """ Test whether or not we can download a url
        :return: True and False
        """
        result = blacksap.get_torrent_file('not_a_valid_url', '/tmp/', 'blacksap.test')
        self.assertFalse(result[0])
        result = blacksap.get_torrent_file('http://jacomputing.net/myip/', '/tmp/', 'blacksap.test')
        self.assertTrue(result[0])
        os.remove('/tmp/blacksap.test')
        pass


class TestCli(unittest.TestCase):

    def setUp(self):
        """ Set stuff up!
        """
        self.runner = CliRunner()

    def test_help(self):
        """ Make sure there aren't any parse errors
        :return: exit_code == 0
        """
        result = self.runner.invoke(blacksap.cli, ['--help'])
        self.assertEqual(result.exit_code, 0)
        pass

    def test_tracking(self):
        """ Test tracking command
        :return: exit_code == 0 and 'feeds tracked' in output
        """
        result = self.runner.invoke(blacksap.cli, ['tracking'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('feeds tracked', result.output)
        pass

    def test_track_valid(self):
        """ Test track command for a valid URL/Feed
        :return: exit_code == 0
        """
        result = self.runner.invoke(blacksap.cli, ['track', 'http://kat.cr/usearch/yify%201080p/?rss=1'])
        self.assertEqual(result.exit_code, 0)
        pass

    def test_track_invalid(self):
        """ Test track command for invalid URL/Feed
        :return: exit_code == 1
        """
        result = self.runner.invoke(blacksap.cli, ['track', 'http://jacomputing.net/'])
        self.assertEqual(result.exit_code, 0)
        pass

    def test_untrack_valid(self):
        """ Test untrack command for valid URL/Feed
        :return: exit_code == 0
        """
        result = self.runner.invoke(blacksap.cli, ['untrack', 'http://kat.cr/usearch/yify%201080p/?rss=1'])
        self.assertEqual(result.exit_code, 0)
        pass

    def test_untrack_invalid(self):
        """ Test untrack command for invalid URL/Feed
        :return: exit_code == 0
        """
        result = self.runner.invoke(blacksap.cli, ['untrack', 'http://jacomputing.net/'])
        self.assertEqual(result.exit_code, 0)
        pass

    def test_run(self):
        """ Test run command
        :return:
        """
        self.test_track_valid()
        os.mkdir('/tmp/blacksap_test/')
        result = self.runner.invoke(blacksap.cli, ['run', '--count', '1', '--force', '-o', '/tmp/blacksap_test/'])
        shutil.rmtree('/tmp/blacksap_test/')
        self.assertEqual(result.exit_code, 0)
        self.assertIn('RSS feeds checked in', result.output)
        pass

    def test_clearcache(self):
        """ Test clearcache command
        :return:
        """
        result = self.runner.invoke(blacksap.cli, ['reset'])
        self.assertEqual(result.exit_code, 0)
        pass


if __name__ == '__main__':
    with warnings.catch_warnings(record=True):
        blacksap.__config__ = '/tmp/blacksap.cfg'
        unittest.main()
        os.remove('/tmp/blacksap.cfg')
