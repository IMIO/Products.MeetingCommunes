# -*- coding: utf-8 -*-
#
# File: testAnnexes.py
#
# GNU General Public License (GPL)
#

from Products.MeetingCommunes.tests.MeetingCommunesTestCase import MeetingCommunesTestCase
from Products.PloneMeeting.tests.testAnnexes import testAnnexes as pmta


class testAnnexes(MeetingCommunesTestCase, pmta):
    ''' '''


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testAnnexes, prefix='test_pm_'))
    return suite
