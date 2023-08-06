##############################################################################
#
# Copyright (c) 2001, 2002 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

import os
import sys
import tempfile
import time
import unittest
import zLOG
import logging

severity_string = {
    -300: 'TRACE',
    -200: 'DEBUG',
    -100: 'BLATHER',
       0: 'INFO',
     100: 'PROBLEM',
     200: 'ERROR',
     300: 'PANIC',
    }


class EventLogTest(unittest.TestCase):
    """Test zLOG with the default implementation."""

    def setUp(self):
        self.f, self.path = tempfile.mkstemp()
        self._severity = 0
        self.loghandler = self.setLog()

    def tearDown(self):
        self.loghandler.close()
        os.close(self.f)
        os.remove(self.path)

    def setLog(self, severity=0):
        logger = logging.getLogger('basic')
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            fmt='------\n%(asctime)s %(name)s %(levelname)s %(message)s',
            datefmt='%Y-%m-%dT%H:%M:%S')
        handler = logging.FileHandler(self.path)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        self._severity = severity
        return handler

    def verifyEntry(self, f, time=None, subsys=None, severity=None,
                    summary=None, detail=None, error=None):
        # skip to the beginning of next entry
        line = f.readline().strip()
        line = f.readline().strip()
        _time, rest = line.split(" ", 1)
        if subsys is not None:
            self.assertIn(subsys, rest, "subsystem mismatch")
        if severity is not None and severity >= self._severity:
            s = severity_string[severity]
            self.assertIn(s, rest, "severity mismatch")
        if summary is not None:
            self.assertIn(summary, rest, "summary mismatch")
        if detail is not None:
            line = f.readline()
            self.assertNotEqual(line.find(detail), -1, "missing detail")
        if error is not None:
            line = f.readline().strip()
            self.assertTrue(line.startswith('Traceback'),
                            "missing traceback")
            last = "%s: %s" % (error[0].__name__, error[1])

    def getLogFile(self):
        return open(self.path, 'r')

    def test_basics(self):
        zLOG.LOG("basic", zLOG.INFO, "summary")
        with self.getLogFile() as f:
            self.verifyEntry(f, subsys="basic", summary="summary")

    def test_detail(self):
        zLOG.LOG("basic", zLOG.INFO, "xxx", "this is a detail")
        with self.getLogFile() as f:
            self.verifyEntry(f, subsys="basic", detail="detail")

    def test_error(self):
        try:
            1 / 0
        except ZeroDivisionError:
            err = sys.exc_info()

        zLOG.LOG("basic", zLOG.INFO, "summary")
        zLOG.LOG("basic", zLOG.ERROR, "raised exception", error=err)
        with self.getLogFile() as f:
            self.verifyEntry(f, subsys="basic", summary="summary")
            self.verifyEntry(f, subsys="basic", severity=zLOG.ERROR, error=err)

    def test_reraise_error(self):
        self.setLog()
        try:
            1 / 0
        except ZeroDivisionError:
            err = sys.exc_info()

        self.assertRaises(ZeroDivisionError, zLOG.LOG, "basic", zLOG.ERROR,
                          "raised exception", error=err, reraise=True)
        with self.getLogFile() as f:
            self.verifyEntry(f, subsys="basic", severity=zLOG.ERROR, error=err)

    def test_bbb(self):
        """ test existence of backwards compatibility methods that do nothing
        """
        zLOG.initialize()
        zLOG.set_initializer(lambda :False)
        zLOG.register_subsystem('foo')
        self.assertTrue('foo' in zLOG._subsystems)

    def test_severity_string(self):
        # severity in mapping
        self.assertEqual(zLOG.severity_string(100), 'PROBLEM(100)')
        # severity not in mapping
        self.assertEqual(zLOG.severity_string(99), '(99)')

    def test_log_time(self):
        now = time.localtime()
        self.assertTrue(zLOG.log_time().startswith(
            '%4.4d-%2.2d-%2.2dT' % time.localtime()[:3]))
