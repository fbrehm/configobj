#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Frank Brehm
@contact: frank@brehm-online.com
@copyright: © 2010 - 2013 by Frank Brehm, Berlin Germany
@license: GPL3
@summary: test script (and module) for unit tests on validation errors
"""

import os
import sys
import logging
import textwrap

try:
    import unittest2 as unittest
except ImportError:
    import unittest

libdir = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), '..'))
sys.path.insert(0, libdir)

import general
from general import ConfigObjTestcase, get_arg_verbose, init_root_logger

log = logging.getLogger(__name__)

#==============================================================================

class TestValidateErrors(ConfigObjTestcase):

    #--------------------------------------------------------------------------
    def setUp(self):

        self.testdir = os.path.join(libdir, 'functionaltests')
        self.ini_file = os.path.join(self.testdir, 'conf.ini')
        self.spec_file = os.path.join(self.testdir, 'conf.spec')

        if not os.path.isfile(self.ini_file):
            self.fail("Ini file %r doesn't exists." % (self.ini_file))
        if not os.path.isfile(self.spec_file):
            self.fail("Spec file %r doesn't exists." % (self.spec_file))

    #--------------------------------------------------------------------------
    def test_import(self):

        log.info("Test importing necessary stuff")

        log.debug("Testing import of configobj ...")
        import configobj

        log.debug("Testing import ConfigObj from configobj ...")
        from configobj import ConfigObj

        log.debug("Testing import get_extra_values from configobj ...")
        from configobj import get_extra_values

        log.debug("Testing import of validate ...")
        import validate

        log.debug("Testing import Validator from validate ...")
        from validate import Validator

    #--------------------------------------------------------------------------
    def test_validate_no_valid_entries(self):

        log.info("Test validate with no valid entries.")

        from configobj import ConfigObj
        from validate import Validator

        log.debug("Using ini file %r.", self.ini_file)
        log.debug("Using spec file %r.", self.spec_file)

        conf = ConfigObj(self.ini_file, configspec = self.spec_file)
        log.debug("ConfigObj: %s", str(conf))

        validator = Validator()
        result = conf.validate(validator)
        log.debug("Result of validation: %r", result)
        self.assertFalse(result)

    #--------------------------------------------------------------------------
    def test_validate_preserve_errors(self):

        log.info("Test validate with preserving errors.")

        from configobj import ConfigObj
        from validate import Validator

        log.debug("Using ini file %r.", self.ini_file)
        log.debug("Using spec file %r.", self.spec_file)

        conf = ConfigObj(self.ini_file, configspec = self.spec_file)
        log.debug("ConfigObj: %s", str(conf))

        validator = Validator()
        result = conf.validate(validator, preserve_errors = True)
        log.debug("Result of validation: %r", result)

        self.assertFalse(result['value'])
        self.assertFalse(result['missing-section'])

        section = result['section']
        self.assertFalse(section['value'])
        self.assertFalse(section['sub-section']['value'])
        self.assertFalse(section['missing-subsection'])

    #--------------------------------------------------------------------------
    def test_validate_extra_values(self):

        log.info("Test validate with extra values.")

        from configobj import ConfigObj
        from validate import Validator

        log.debug("Using ini file %r.", self.ini_file)
        log.debug("Using spec file %r.", self.spec_file)

        conf = ConfigObj(self.ini_file, configspec = self.spec_file)

        conf.validate(Validator(), preserve_errors = True)
        log.debug("ConfigObj after validate: %s", str(conf))

        self.assertEqual(conf.extra_values, ['extra', 'extra-section'])

        self.assertEqual(conf['section'].extra_values, ['extra-sub-section'])
        self.assertEqual(conf['section']['sub-section'].extra_values,
                         ['extra'])

    #--------------------------------------------------------------------------
    def test_get_extra_values(self):

        log.info("Test getting extra values.")

        from configobj import ConfigObj, get_extra_values
        from validate import Validator

        log.debug("Using ini file %r.", self.ini_file)
        log.debug("Using spec file %r.", self.spec_file)

        conf = ConfigObj(self.ini_file, configspec = self.spec_file)

        conf.validate(Validator(), preserve_errors = True)
        log.debug("ConfigObj after validate: %s", str(conf))

        expected = sorted([
            ((), 'extra'),
            ((), 'extra-section'),
            (('section', 'sub-section'), 'extra'),
            (('section',), 'extra-sub-section'),
        ])
        log.debug("Expected extra values: %r.", expected)

        extra_values = get_extra_values(conf)
        log.debug("Got extra values: %r.", extra_values)

        self.assertEqual(sorted(extra_values), expected)

#==============================================================================

if __name__ == '__main__':

    verbose = get_arg_verbose()
    if verbose is None:
        verbose = 0
    init_root_logger(verbose)

    log.info("Starting tests ...")

    suite = unittest.TestSuite()

    suite.addTest(TestValidateErrors('test_import', verbose))
    suite.addTest(TestValidateErrors('test_validate_no_valid_entries', verbose))
    suite.addTest(TestValidateErrors('test_validate_preserve_errors', verbose))
    suite.addTest(TestValidateErrors('test_validate_extra_values', verbose))
    suite.addTest(TestValidateErrors('test_get_extra_values', verbose))

    runner = unittest.TextTestRunner(verbosity = verbose)

    result = runner.run(suite)

#==============================================================================

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
