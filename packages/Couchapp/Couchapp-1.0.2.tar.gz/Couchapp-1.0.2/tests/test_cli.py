#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2009 Benoit Chesneau <benoitc@e-engura.org>
#
# This software is licensed as described in the file LICENSE, which
# you should have received as part of this distribution.

import os
import tempfile
import shutil
import sys
import unittest2 as unittest
from testconfig import config

from couchapp.errors import ResourceNotFound
from couchapp.client import Database
from couchapp.util import popen3, deltree

couchapp_dir = os.path.join(os.path.dirname(__file__), '../')
couchapp_cli = os.path.join(os.path.dirname(__file__), '../bin/couchapp')
try:
    url = config['host']['url']
except KeyError:
    url = 'http://127.0.0.1:5984/'


def _tempdir():
    f, fname = tempfile.mkstemp()
    os.close(f)
    os.unlink(fname)
    return fname


class CliTestCase(unittest.TestCase):

    def setUp(self):
        self.db = Database(url + 'couchapp-test', create=True)

        self.tempdir = _tempdir()
        os.makedirs(self.tempdir)
        self.app_dir = os.path.join(self.tempdir, "my-app")
        self.cmd = "cd %s && couchapp" % self.tempdir
        self.startdir = os.getcwd()

    def tearDown(self):
        self.db.delete()
        deltree(self.tempdir)
        os.chdir(self.startdir)

    def _make_testapp(self):
        testapp_path = os.path.join(os.path.dirname(__file__), 'testapp')
        shutil.copytree(testapp_path, self.app_dir)

    def _retrieve_ddoc(self):
        # any design doc created ?
        design_doc = None
        try:
            design_doc = self.db.open_doc('_design/my-app')
        except ResourceNotFound:
            pass
        self.assertIsNotNone(design_doc)
        return design_doc

    def testGenerate(self):
        os.chdir(self.tempdir)
        (child_stdin, child_stdout, child_stderr) = popen3("%s generate my-app"
                                                           % self.cmd)
        appdir = os.path.join(self.tempdir, 'my-app')
        self.assertTrue(os.path.isdir(appdir))
        cfile = os.path.join(appdir, '.couchapprc')
        self.assertTrue(os.path.isfile(cfile))

        self.assertTrue(os.path.isdir(os.path.join(appdir, '_attachments')))
        self.assertTrue(os.path.isfile(os.path.join(appdir, '_attachments',
                                                    'index.html')))
        self.assertTrue(os.path.isfile(os.path.join(self.app_dir,
                                                    '_attachments',
                                                    'style', 'main.css')))
        self.assertTrue(os.path.isdir(os.path.join(appdir, 'views')))
        self.assertTrue(os.path.isdir(os.path.join(appdir, 'shows')))
        self.assertTrue(os.path.isdir(os.path.join(appdir, 'lists')))

    def testPush(self):
        self._make_testapp()
        (child_stdin, child_stdout, child_stderr) = \
            popen3("%s push -v my-app %scouchapp-test" % (self.cmd, url))

        design_doc = self._retrieve_ddoc()

        # should create view
        self.assertIn('function', design_doc['views']['example']['map'])

        # should use macros
        self.assertIn('stddev', design_doc['views']['example']['map'])
        self.assertIn('ejohn.org', design_doc['shows']['example-show'])
        self.assertIn('included by foo.js',
                      design_doc['shows']['example-show'])

        # should create index
        content_type = design_doc['_attachments']['index.html']['content_type']
        self.assertEqual(content_type, 'text/html')

        # should create manifest
        self.assertIn('foo/', design_doc['couchapp']['manifest'])

        # should push and macro the doc shows
        self.assertIn('Generated CouchApp Form Template',
                      design_doc['shows']['example-show'])

        # should push and macro the view lists
        self.assertIn('Test XML Feed', design_doc['lists']['feed'])

        # should allow deeper includes
        self.assertNotIn('"helpers"', design_doc['shows']['example-show'])

        # deep require macros
        self.assertNotIn('"template"', design_doc['shows']['example-show'])
        self.assertIn('Resig', design_doc['shows']['example-show'])

    def testPushNoAtomic(self):
        self._make_testapp()
        (child_stdin, child_stdout, child_stderr) = \
            popen3("%s push --no-atomic my-app %scouchapp-test" % (self.cmd,
                                                                   url))

        design_doc = self._retrieve_ddoc()

        # there are 3 revisions (1 doc creation + 2 attachments)
        self.assertTrue(design_doc['_rev'].startswith('3-'))

        # should create view
        self.assertIn('function', design_doc['views']['example']['map'])

        # should use macros
        self.assertIn('stddev', design_doc['views']['example']['map'])
        self.assertIn('ejohn.org', design_doc['shows']['example-show'])

        # should create index
        content_type = design_doc['_attachments']['index.html']['content_type']
        self.assertEqual(content_type, 'text/html')

        # should create manifest
        self.assertIn('foo/', design_doc['couchapp']['manifest'])

        # should push and macro the doc shows
        self.assertIn('Generated CouchApp Form Template',
                      design_doc['shows']['example-show'])

        # should push and macro the view lists
        self.assertIn('Test XML Feed', design_doc['lists']['feed'])

        # should allow deeper includes
        self.assertNotIn('"helpers"', design_doc['shows']['example-show'])

        # deep require macros
        self.assertNotIn('"template"', design_doc['shows']['example-show'])
        self.assertIn('Resig', design_doc['shows']['example-show'])

    def testClone(self):
        self._make_testapp()
        (child_stdin, child_stdout, child_stderr) = \
            popen3("%s push -v my-app %scouchapp-test" % (self.cmd, url))

        design_doc = self._retrieve_ddoc()

        app_dir = os.path.join(self.tempdir, "couchapp-test")

        (child_stdin, child_stdout, child_stderr) = \
            popen3("%s clone %s %s"
                   % (self.cmd,
                      url + "couchapp-test/_design/my-app",
                      app_dir))

        # should create .couchapprc
        self.assertTrue(os.path.isfile(os.path.join(app_dir, ".couchapprc")))

        # should clone the views
        self.assertTrue(os.path.isdir(os.path.join(app_dir, "views")))

        # should create foo/bar.txt file
        self.assertTrue(os.path.isfile(os.path.join(app_dir, 'foo/bar.txt')))

        # should create lib/helpers/math.js file
        self.assertTrue(os.path.isfile(os.path.join(app_dir,
                                                    'lib/helpers/math.js')))

        # should work when design doc is edited manually
        design_doc['test.txt'] = "essai"

        design_doc = self.db.save_doc(design_doc)

        deltree(app_dir)
        (child_stdin, child_stdout, child_stderr) = \
            popen3("%s clone %s %s"
                   % (self.cmd,
                      url + "couchapp-test/_design/my-app",
                      app_dir))
        self.assertTrue(os.path.isfile(os.path.join(app_dir, 'test.txt')))

        # should work when a view is added manually
        design_doc["views"]["more"] = {"map":
                                       "function(doc) { emit(null, doc); }"}

        design_doc = self.db.save_doc(design_doc)

        deltree(app_dir)
        (child_stdin, child_stdout, child_stderr) = \
            popen3("%s clone %s %s"
                   % (self.cmd,
                      url + "couchapp-test/_design/my-app",
                      app_dir))
        self.assertTrue(os.path.isfile(os.path.join(app_dir,
                                                    'views/example/map.js')))

        # should work without manifest
        del design_doc['couchapp']['manifest']
        design_doc = self.db.save_doc(design_doc)
        deltree(app_dir)
        (child_stdin, child_stdout, child_stderr) = \
            popen3("%s clone %s %s"
                   % (self.cmd,
                      url + "couchapp-test/_design/my-app",
                      app_dir))
        self.assertTrue(os.path.isfile(os.path.join(app_dir,
                                                    'views/example/map.js')))

        # should create foo/bar without manifest
        self.assertTrue(os.path.isfile(os.path.join(app_dir, 'foo/bar')))

        # should create lib/helpers.json without manifest
        self.assertTrue(os.path.isfile(os.path.join(app_dir,
                                                    'lib/helpers.json')))

    def testPushApps(self):
        os.chdir(self.tempdir)
        docsdir = os.path.join(self.tempdir, 'docs')
        os.makedirs(docsdir)

        # create 2 apps
        (child_stdin, child_stdout, child_stderr) = \
            popen3("%s generate docs/app1" % self.cmd)
        (child_stdin, child_stdout, child_stderr) = \
            popen3("%s generate docs/app2" % self.cmd)

        (child_stdin, child_stdout, child_stderr) = \
            popen3("%s pushapps docs/ %scouchapp-test"
                   % (self.cmd, url))

        alldocs = self.db.all_docs()['rows']
        self.assertEqual(len(alldocs), 2)
        self.assertEqual('_design/app1', alldocs[0]['id'])

    def testPushDocs(self):
        os.chdir(self.tempdir)
        docsdir = os.path.join(self.tempdir, 'docs')
        os.makedirs(docsdir)

        # create 2 apps
        (child_stdin, child_stdout, child_stderr) = \
            popen3("%s generate docs/app1" % self.cmd)
        (child_stdin, child_stdout, child_stderr) = \
            popen3("%s generate docs/app2" % self.cmd)

        (child_stdin, child_stdout, child_stderr) = \
            popen3("%s pushdocs docs/ %scouchapp-test"
                   % (self.cmd, url))

        alldocs = self.db.all_docs()['rows']

        self.assertEqual(len(alldocs), 2)

        self.assertEqual('_design/app1', alldocs[0]['id'])


if __name__ == '__main__':
    unittest.main()
