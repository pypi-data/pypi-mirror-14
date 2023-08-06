#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This software is licensed as described in the file LICENSE, which
# you should have received as part of this distribution.

import unittest2 as unittest
import mock
import os

class CompressTest(unittest.TestCase):

    def test_compress_js(self):
        from couchapp.config import Config
        config = Config()
        config.conf['compress'] = {'js': {'foo':['shows/example-show.js']}}
        with mock.patch('couchapp.hooks.compress.default.compress', return_value='foo') as mock_compress:
            from couchapp.hooks.compress import Compress
            compress = Compress(os.path.join(os.path.dirname(__file__), 'testapp'))
            compress.conf = config
            with mock.patch('couchapp.util.write'):
                compress.run()
        self.assertTrue(mock_compress.called, 'Default compressor has been called')

    def test_our_jsmin_loading(self):
        orig_import = __import__

        def import_mock(name, *args):
            if name == 'jsmin':
                raise ImportError()
            return orig_import(name, *args)

        with mock.patch('__builtin__.__import__', side_effect=import_mock):
            with mock.patch('couchapp.hooks.compress.jsmin.jsmin', return_value='foo'):
                from couchapp.hooks.compress import default
                result = default.compress('bar')
        self.assertEqual(result, 'foo', 'Our module is called when it is not installed in the system')

    def test_system_jsmin_loading(self):
        orig_import = __import__

        def import_mock(name, *args):
            if name == 'couchapp.hooks.compress.jsmin':
                raise ImportError()
            return orig_import(name, *args)

        with mock.patch('__builtin__.__import__', side_effect=import_mock):
            with mock.patch('jsmin.jsmin', return_value='foo'):
                from couchapp.hooks.compress import default
                result = default.compress('bar')
        self.assertEqual(result, 'foo', 'The system module is called when it is installed')


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
