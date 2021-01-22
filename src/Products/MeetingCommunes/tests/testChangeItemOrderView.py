# -*- coding: utf-8 -*-
#
# File: testChangeItemOrderView.py
#
# GNU General Public License (GPL)
#

from Products.MeetingCommunes.tests.MeetingCommunesTestCase import MeetingCommunesTestCase
from Products.PloneMeeting.tests.testChangeItemOrderView import testChangeItemOrderView as pmciov


class testChangeItemOrderView(MeetingCommunesTestCase, pmciov):
    '''Tests the ChangeItemOrderView class methods.'''


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testChangeItemOrderView, prefix='test_pm_'))
    return suite
