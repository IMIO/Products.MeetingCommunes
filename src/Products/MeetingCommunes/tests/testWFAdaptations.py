# -*- coding: utf-8 -*-

from Products.MeetingCommunes.tests.MeetingCommunesTestCase import MeetingCommunesTestCase
from Products.PloneMeeting.tests.testWFAdaptations import testWFAdaptations as pmtwfa


class testWFAdaptations(MeetingCommunesTestCase, pmtwfa):
    '''See doc string in PloneMeeting.tests.testWFAdaptations.'''


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testWFAdaptations, prefix='test_pm_'))
    return suite
