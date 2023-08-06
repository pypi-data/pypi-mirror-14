# -*- coding: utf-8 -*-

import os

from couchapp.util import discover_apps, iscouchapp, rcpath, split_path

from mock import patch


@patch('couchapp.util.user_rcpath')
@patch('couchapp.util._rcpath')
def test_rcpath_cached(_rcpath, user_rcpath):
    '''
    Global ``_rcpath`` is not None already
    '''
    assert _rcpath == rcpath()
    assert not user_rcpath.called


@patch.dict('couchapp.util.os.environ', clear=True)
@patch('couchapp.util.user_rcpath', return_value=['/mock/couchapp.conf'])
def test_rcpath_empty_env(user_rcpath):
    '''
    Empty ``COUCHAPPCONF_PATH``
    '''
    import couchapp.util as util
    util._rcpath = None
    assert rcpath() == ['/mock/couchapp.conf'], rcpath()
    assert user_rcpath.called


@patch.dict('couchapp.util.os.environ',
            {'COUCHAPPCONF_PATH': '/mock:/tmp/fake.conf'})
@patch('couchapp.util.os.listdir')
@patch('couchapp.util.os.path.isdir')
@patch('couchapp.util.user_rcpath')
def test_rcpath_env(user_rcpath, isdir, listdir):
    '''
    With ``COUCHAPPCONF_PATH`` set
    '''
    import couchapp.util as util
    util._rcpath = None

    def _isdir(path):
        return True if path == '/mock' else False

    def _listdir(path):
        return ['foo', 'bar', 'couchapp.conf'] if path == '/mock' else []

    isdir.side_effect = _isdir
    listdir.side_effect = _listdir

    assert rcpath() == ['/mock/couchapp.conf', '/tmp/fake.conf'], rcpath()
    assert not user_rcpath.called


@patch('couchapp.util.os.path.isfile', return_value=True)
def test_iscouchapp(isfile):
    assert iscouchapp('/mock_dir') == True
    isfile.assert_called_with('/mock_dir/.couchapprc')


@patch('couchapp.util.os.listdir', return_value=['foo'])
@patch('couchapp.util.os.path.isdir', return_value=True)
@patch('couchapp.util.iscouchapp', return_value=True)
def test_discover_apps(iscouchapp_, isdir, listdir):
    assert discover_apps('/mock_dir') == ['/mock_dir/foo']
    isdir.assert_called_with('/mock_dir/foo')
    listdir.assert_called_with('/mock_dir')


@patch('couchapp.util.os.listdir', return_value=['foo'])
@patch('couchapp.util.os.path.isdir', return_value=True)
@patch('couchapp.util.iscouchapp', return_value=True)
def test_discover_apps_relative_path(iscouchapp_, isdir, listdir):
    assert discover_apps('mock_dir') == ['mock_dir/foo']
    isdir.assert_called_with('mock_dir/foo')
    listdir.assert_called_with('mock_dir')


@patch('couchapp.util.os.listdir', return_value=['.git', 'foo'])
@patch('couchapp.util.os.path.isdir', return_value=True)
@patch('couchapp.util.iscouchapp', return_value=True)
def test_discover_apps_hidden_file(iscouchapp_, isdir, listdir):
    '''
    Test case for a dir including hidden file
    '''
    assert discover_apps('mock_dir') == ['mock_dir/foo']
    isdir.assert_called_with('mock_dir/foo')
    listdir.assert_called_with('mock_dir')


def test_split_path_rel():
    '''
    Test case for util.split_path with relative path
    '''
    assert split_path('foo/bar') == ['foo', 'bar']


def test_split_path_abs():
    '''
    Test case for util.split_path with abs path
    '''
    path = os.path.realpath('/foo/bar')
    assert split_path(path) == [os.path.realpath('/foo'), 'bar']
