#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Frank Brehm
@contact: frank@brehm-online.com
@copyright: © 2010 - 2013 by Frank Brehm, Berlin Germany
@license: GPL3
@summary: test script (and module) for unit tests on configobj
"""

import os
import sys
import logging

try:
    import unittest2 as unittest
except ImportError:
    import unittest

catch_warnings = None
try:
    import warnings
    # for Python2 >= 2.6 and Python3
    from warnings import catch_warnings
except ImportError:
    catch_warnings = None

libdir = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), '..'))
sys.path.insert(0, libdir)

import general
from general import ConfigObjTestcase, get_arg_verbose, init_root_logger

log = logging.getLogger(__name__)

#==============================================================================

class TestConfigObj(ConfigObjTestcase):

    #--------------------------------------------------------------------------
    def setUp(self):
        pass

    #--------------------------------------------------------------------------
    def test_import(self):

        log.info("Testing import of configobj ...")
        import configobj

        log.info("Testing import ConfigObj from configobj ...")
        from configobj import ConfigObj

    #--------------------------------------------------------------------------
    def test_order_preserved(self):

        import configobj
        from configobj import ConfigObj

        log.info("Testing preserved order ...")

        c = ConfigObj()
        c['a'] = 1
        c['b'] = 2
        c['c'] = 3
        c['section'] = {}
        c['section']['a'] = 1
        c['section']['b'] = 2
        c['section']['c'] = 3
        c['section']['section'] = {}
        c['section']['section2'] = {}
        c['section']['section3'] = {}
        c['section2'] = {}
        c['section3'] = {}

        log.debug("ConfigObj 1: %s", str(c))

        c2 = ConfigObj(c)

        log.debug("ConfigObj 2: %s", str(c2))

        self.assertEqual(c2.scalars, ['a', 'b', 'c'])
        self.assertEqual(c2.sections, ['section', 'section2', 'section3'])
        self.assertEqual(c2['section'].scalars, ['a', 'b', 'c'])
        self.assertEqual(c2['section'].sections, ['section', 'section2', 'section3'])

        self.assertFalse(c['section'] is c2['section'])
        self.assertFalse(c['section']['section'] is c2['section']['section'])

    #--------------------------------------------------------------------------
    @unittest.skipIf(catch_warnings is None,
            "catch_warnings() from module warnings not available")
    def test_options_deprecation(self):

        import configobj
        from configobj import ConfigObj

        log.info("Test for DeprecationWarning ...")

        with catch_warnings(record = True) as w:

            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")

            # Trigger a warning.
            ConfigObj(options = {})

            self.assertEqual(len(w), 1)

            # unpack the only member of log
            warning = w[0]

            # check the warning
            log.debug("Got warning: %r", warning.message)
            self.assertEqual(warning.category, DeprecationWarning)
            self.assertIn("deprecated", str(warning.message))

    #--------------------------------------------------------------------------
    def test_list_members(self):

        import configobj
        from configobj import ConfigObj

        log.info("Testing list members ...")
        c = ConfigObj()
        c['a'] = []
        c['a'].append('foo')
        self.assertEqual(c['a'], ['foo'])

#==============================================================================

if __name__ == '__main__':

    verbose = get_arg_verbose()
    if verbose is None:
        verbose = 0
    init_root_logger(verbose)

    log.info("Starting tests ...")

    suite = unittest.TestSuite()

    suite.addTest(TestConfigObj('test_import', verbose))
    suite.addTest(TestConfigObj('test_order_preserved', verbose))
    suite.addTest(TestConfigObj('test_options_deprecation', verbose))
    suite.addTest(TestConfigObj('test_list_members', verbose))

    runner = unittest.TextTestRunner(verbosity = verbose)

    result = runner.run(suite)

#==============================================================================

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
