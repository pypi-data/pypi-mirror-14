#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_vxscreenshots
----------------------------------

Tests for `vxscreenshots` module.
"""

import unittest

from vxscreenshots import vxscreenshots
from vxscreenshots import config
from vxscreenshots import watch


class TestVxscreenshots(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_000_something(self):
        pass

    def test_001_config(self):
        c = config.read_config()
        self.assertTrue(isinstance(c.get('vxscreenshots.database'), str))

    def test_002_icon(self):
        appx = vxscreenshots.AppShareSmart('Name App')
        pass
    def test_003_watch(self):
        s3 = watch.S3Element('test.example.com', 'nhomar')

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
