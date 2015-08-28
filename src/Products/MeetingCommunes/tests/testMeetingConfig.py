# -*- coding: utf-8 -*-
#
# File: testMeetingConfig.py
#
# Copyright (c) 2007-2013 by Imio.be
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
from Products.PloneMeeting.tests.testMeetingConfig import testMeetingConfig as pmtmc


class testMeetingConfig(MeetingCommunesTestCase, pmtmc):
    '''Tests the MeetingConfig class methods.'''

    def test_subproduct_call_Validate_shortName(self):
        '''Run the test_pm_Validate_shortName from PloneMeeting.'''
        pmtmc.test_pm_Validate_shortName(self)

    def test_subproduct_call_Validate_customAdvisersCanNotChangeUsedConfig(self):
        '''Run the test_pm_searchItemsWithFilters from PloneMeeting.'''
        pmtmc.test_pm_Validate_customAdvisersCanNotChangeUsedConfig(self)

    def test_subproduct_call_Validate_customAdvisersDateColumns(self):
        '''Run the test_pm_searchItemsWithFilters from PloneMeeting.'''
        pmtmc.test_pm_Validate_customAdvisersDateColumns(self)

    def test_subproduct_call_Validate_customAdvisersDelayColumn(self):
        '''Run the test_pm_searchItemsWithFilters from PloneMeeting.'''
        pmtmc.test_pm_Validate_customAdvisersDelayColumn(self)

    def test_subproduct_call_Validate_transitionsForPresentingAnItem(self):
        '''Run the test_pm_validateTransitionsForPresentingAnItem from PloneMeeting.'''
        pmtmc.test_pm_Validate_transitionsForPresentingAnItem(self)

    def test_subproduct_call_Validate_customAdvisersIsLinkedToPreviousRowDelayAware(self):
        '''Run the test_pm_Validate_customAdvisersIsLinkedToPreviousRowDelayAware from PloneMeeting.'''
        pmtmc.test_pm_Validate_customAdvisersIsLinkedToPreviousRowDelayAware(self)

    def test_subproduct_call_Validate_customAdvisersIsLinkedToPreviousRowIsUsed(self):
        '''Run the test_pm_Validate_customAdvisersIsLinkedToPreviousRowIsUsed from PloneMeeting.'''
        pmtmc.test_pm_Validate_customAdvisersIsLinkedToPreviousRowIsUsed(self)

    def test_subproduct_call_Validate_customAdvisersEnoughData(self):
        '''Run the test_pm_Validate_customAdvisersEnoughData from PloneMeeting.'''
        pmtmc.test_pm_Validate_customAdvisersEnoughData(self)

    def test_subproduct_call_Validate_customAdvisersAvailableOn(self):
        '''Run the test_pm_Validate_customAdvisersAvailableOn from PloneMeeting.'''
        pmtmc.test_pm_Validate_customAdvisersAvailableOn(self)

    def test_subproduct_call_Validate_insertingMethodsOnAddItem(self):
        '''Run the test_pm_Validate_insertingMethodsOnAddItem from PloneMeeting.'''
        pmtmc.test_pm_Validate_insertingMethodsOnAddItem(self)

    def test_subproduct_call_Validate_meetingConfigsToCloneTo(self):
        '''Run the test_pm_Validate_meetingConfigsToCloneTo from PloneMeeting.'''
        pmtmc.test_pm_Validate_meetingConfigsToCloneTo(self)

    def test_subproduct_call_GetAvailablePodTemplates(self):
        '''Run the test_pm_GetAvailablePodTemplates from PloneMeeting.'''
        pmtmc.test_pm_GetAvailablePodTemplates(self)

    def test_subproduct_call_AddingExistingSearchDoesNotBreak(self):
        '''Run the test_pm_AddingExistingSearchDoesNotBreak from PloneMeeting.'''
        pmtmc.test_pm_AddingExistingSearchDoesNotBreak(self)

    def test_subproduct_call_MeetingManagersMayEditHarmlessConfigFields(self):
        '''Run the test_pm_MeetingManagersMayEditHarmlessConfigFields from PloneMeeting.'''
        pmtmc.test_pm_MeetingManagersMayEditHarmlessConfigFields(self)

    def test_subproduct_call_Validate_certifiedSignatures(self):
        '''Run the test_pm_Validate_certifiedSignatures from PloneMeeting.'''
        pmtmc.test_pm_Validate_certifiedSignatures(self)

    def test_subproduct_call_MeetingConfigGroupsCreatedCorrectly(self):
        '''Run the test_pm_MeetingConfigGroupsCreatedCorrectly from PloneMeeting.'''
        pmtmc.test_pm_MeetingConfigGroupsCreatedCorrectly(self)

    def test_subproduct_call_ItemIconColor(self):
        '''Run the test_pm_ItemIconColor from PloneMeeting.'''
        pmtmc.test_pm_ItemIconColor(self)

    def test_subproduct_call_CanNotRemoveUsedMeetingConfig(self):
        '''Run the test_pm_CanNotRemoveUsedMeetingConfig from PloneMeeting.'''
        pmtmc.test_pm_CanNotRemoveUsedMeetingConfig(self)

    def test_subproduct_call_SynchSearches(self):
        '''Run the test_pm_SynchSearches from PloneMeeting.'''
        pmtmc.test_pm_SynchSearches(self)

    def test_subproduct_call_GetRecurringItems(self):
        '''Run the test_pm_GetRecurringItems from PloneMeeting.'''
        pmtmc.test_pm_GetRecurringItems(self)

    def test_subproduct_call_NewDashboardCollectionColumns(self):
        '''Run the test_pm_NewDashboardCollectionColumns from PloneMeeting.'''
        pmtmc.test_pm_NewDashboardCollectionColumns(self)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testMeetingConfig, prefix='test_subproduct_'))
    return suite
