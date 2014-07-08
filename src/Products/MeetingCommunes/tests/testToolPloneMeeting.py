# -*- coding: utf-8 -*-
#
# File: testToolPloneMeeting.py
#
# Copyright (c) 2007-2012 by PloneGov
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

from Products.MeetingCommunes.tests.MeetingCommunesTestCase import \
    MeetingCommunesTestCase
from Products.PloneMeeting.tests.testToolPloneMeeting import testToolPloneMeeting as pmtt


class testToolPloneMeeting(MeetingCommunesTestCase, pmtt):
    '''Tests the ToolPloneMeeting class methods.'''

    def test_subproduct_call_GetMeetingGroup(self):
        '''Run the testGetMeetingGroup from PloneMeeting.'''
        self.test_pm_GetMeetingGroup()

    def test_subproduct_call_MoveMeetingGroups(self):
        '''Run the testMoveMeetingGroups from PloneMeeting.'''
        self.test_pm_MoveMeetingGroups()

    def test_subproduct_call_CloneItem(self):
        '''Run the testCloneItem from PloneMeeting.'''
        self.test_pm_CloneItem()

    def test_subproduct_call_CloneItemWithContent(self):
        '''Run the testCloneItemWithContent from PloneMeeting.'''
        self.test_pm_CloneItemWithContent()

    def test_subproduct_call_CloneItemWithContentNotRemovableByPermission(self):
        '''Run the testCloneItemWithContentNotRemovableByPermission from PloneMeeting.'''
        self.test_pm_CloneItemWithContentNotRemovableByPermission()

    def test_subproduct_call_PasteItems(self):
        '''Run the testPasteItems from PloneMeeting.'''
        self.test_pm_PasteItems()

    def test_subproduct_call_ShowPloneMeetingTab(self):
        '''Run the testShowPloneMeetingTab from PloneMeeting.'''
        self.test_pm_ShowPloneMeetingTab()

    def test_subproduct_call_SetupProcessForCreationFlag(self):
        '''Run the test_pm_SetupProcessForCreationFlag from PloneMeeting.'''
        self.test_pm_SetupProcessForCreationFlag()

    def test_subproduct_call_UpdateMeetingFileTypesAfterSentToOtherMeetingConfig(self):
        '''Run the test_pm_UpdateMeetingFileTypesAfterSentToOtherMeetingConfig from PloneMeeting.'''
        self.test_pm_UpdateMeetingFileTypesAfterSentToOtherMeetingConfig()

    def test_subproduct_call_UpdateDelayAwareAdvices(self):
        '''Run the test_pm_getAutomaticAdvisers from PloneMeeting.'''
        self.test_pm_UpdateDelayAwareAdvices(self)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testToolPloneMeeting, prefix='test_subproduct_'))
    return suite
