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

    def test_mc_VerifyTestNumbers(self):
        """
            We verify that there are the same test methods in original product and this sub-product
        """
        tpm = self.getTestMethods(pmtt, 'test')
        tmc = self.getTestMethods(testToolPloneMeeting, 'test_mc_call_')
        missing = []
        for key in tpm:
            key2 = key.replace('test', 'test_mc_call_')
            if not key2 in tmc:
                missing.append(key)
        if len(missing):
            self.fail("missing test methods %s from PloneMeeting test class '%s'" % (missing, 'testToolPloneMeeting'))

    def test_mc_call_GetMeetingGroup(self):
        '''Run the testGetMeetingGroup from PloneMeeting.'''
        self.testGetMeetingGroup()

    def test_mc_call_MoveMeetingGroups(self):
        '''Run the testMoveMeetingGroups from PloneMeeting.'''
        self.testMoveMeetingGroups()

    def test_mc_call_CloneItem(self):
        '''Run the testCloneItem from PloneMeeting.'''
        self.testCloneItem()

    def test_mc_call_CloneItemWithContent(self):
        '''Run the testCloneItemWithContent from PloneMeeting.'''
        self.testCloneItemWithContent()

    def test_mc_call_CloneItemWithContentNotRemovableByPermission(self):
        '''Run the testCloneItemWithContentNotRemovableByPermission from PloneMeeting.'''
        self.testCloneItemWithContentNotRemovableByPermission()

    def test_mc_call_PasteItems(self):
        '''Run the testPasteItems from PloneMeeting.'''
        self.testPasteItems()

    def test_mc_call_ShowPloneMeetingTab(self):
        '''Run the testShowPloneMeetingTab from PloneMeeting.'''
        self.testShowPloneMeetingTab()

    def test_mc_call_SetupProcessForCreationFlag(self):
        '''Run the testSetupProcessForCreationFlag from PloneMeeting.'''
        self.testSetupProcessForCreationFlag()


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testToolPloneMeeting, prefix='test_mc_'))
    return suite
