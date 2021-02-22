# -*- coding: utf-8 -*-
#
# File: testMeeting.py
#
# GNU General Public License (GPL)
#

from Products.MeetingCommunes.tests.MeetingCommunesTestCase import MeetingCommunesTestCase
from Products.PloneMeeting.tests.testMeeting import testMeetingType as pmtmt


class testMeetingType(MeetingCommunesTestCase, pmtmt):
    """
        Tests the Meeting class methods.
    """


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testMeetingType, prefix='test_pm_'))
    return suite
