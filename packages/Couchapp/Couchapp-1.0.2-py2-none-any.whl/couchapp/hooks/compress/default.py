# -*- coding: utf-8 -*-
#
# This file is part of couchapp released under the Apache 2 license.
# See the NOTICE for more information.
from __future__ import absolute_import

__about__ = 'jsmin'

def compress(js):
    try:
        import jsmin
    except:
        import couchapp.hooks.compress.jsmin as jsmin

    return jsmin.jsmin(js)
