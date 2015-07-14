# -*- coding: utf-8 -*-
#
# File: testMeetingConfig.py
#
# Copyright (c) 2015 by Imio.be
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

from Products.MeetingCommunes.tests.MeetingCommunesTestCase import MeetingCommunesTestCase
from Products.PloneMeeting.tests.testSearches import testSearches as pmts


class testSearches(MeetingCommunesTestCase, pmts):
    """Test searches."""

    def test_subproduct_call_DefaultSelectedSearch(self):
        '''Run the test_pm_DefaultSelectedSearch from PloneMeeting.'''
        pmts.test_pm_DefaultSelectedSearch(self)

    def test_subproduct_call_SearchItemsToAdviceAdapter(self):
        '''Run the test_pm_SearchItemsToAdviceAdapter from PloneMeeting.'''
        pmts.test_pm_SearchItemsToAdviceAdapter(self)

    def test_subproduct_call_SearchAdvisedItems(self):
        '''Run the test_pm_SearchAdvisedItems from PloneMeeting.'''
        pmts.test_pm_SearchAdvisedItems(self)

    def test_subproduct_call_SearchAdvisedItemsWithDelay(self):
        '''Run the test_pm_SearchAdvisedItemsWithDelay from PloneMeeting.'''
        pmts.test_pm_SearchAdvisedItemsWithDelay(self)

    def test_subproduct_call_SearchItemsInCopy(self):
        '''Run the test_pm_SearchItemsInCopy from PloneMeeting.'''
        pmts.test_pm_SearchItemsInCopy(self)

    def test_subproduct_call_SearchMyItemsTakenOver(self):
        '''Run the test_pm_SearchMyItemsTakenOver from PloneMeeting.'''
        pmts.test_pm_SearchMyItemsTakenOver(self)

    def test_subproduct_call_SearchItemsToValidateOfHighestHierarchicLevel(self):
        '''Run the test_pm_SearchItemsToValidateOfHighestHierarchicLevel from PloneMeeting.'''
        pmts.test_pm_SearchItemsToValidateOfHighestHierarchicLevel(self)

    def test_subproduct_call_SearchItemsToValidateOfMyReviewerGroups(self):
        '''Run the test_pm_SearchItemsToValidateOfMyReviewerGroups from PloneMeeting.'''
        pmts.test_pm_SearchItemsToValidateOfMyReviewerGroups(self)

    def test_subproduct_call_SearchItemsToValidateOfEveryReviewerLevelsAndLowerLevels(self):
        '''Run the test_pm_SearchItemsToValidateOfEveryReviewerLevelsAndLowerLevels from PloneMeeting.'''
        pmts.test_pm_SearchItemsToValidateOfEveryReviewerLevelsAndLowerLevels(self)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testSearches, prefix='test_subproduct_'))
    return suite
