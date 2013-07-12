# -*- coding: utf-8 -*-
#
# File: testMeetingItem.py
#
# Copyright (c) 2007-2012 by CommunesPlone.org
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

from DateTime import DateTime
from AccessControl import Unauthorized
from plone.app.testing import login
from Products.CMFCore.utils import getToolByName
from Products.MeetingCommunes.tests.MeetingCommunesTestCase import \
    MeetingCommunesTestCase
from Products.PloneMeeting.tests.testMeetingItem import testMeetingItem as pmtmi


class testMeetingItem(MeetingCommunesTestCase, pmtmi):
    """
        Tests the MeetingItem class methods.
    """

    def test_subproduct_call_ListProposingGroup(self):
        """
           Run the testListProposingGroup from PloneMeeting
        """
        #we do the test for the college config
        self.meetingConfig = getattr(self.tool, 'meeting-config-college')
        pmtmi.test_pm_ListProposingGroup(self)
        #we do the test for the council config
        self.meetingConfig = getattr(self.tool, 'meeting-config-council')
        pmtmi.test_pm_ListProposingGroup(self)

    def test_subproduct_call_UsedColorSystemGetColoredLink(self):
        """
           Test the selected system of color while getting a colored link
        """
        #we do the test for the college config
        self.meetingConfig = getattr(self.tool, 'meeting-config-college')
        pmtmi.test_pm_UsedColorSystemGetColoredLink(self)
        #we do the test for the council config
        self.meetingConfig = getattr(self.tool, 'meeting-config-council')
        pmtmi.test_pm_UsedColorSystemGetColoredLink(self)

    def test_subproduct_call_UsedColorSystemShowColors(self):
        """
           Test the selected system of color
        """
        #we do the test for the college config
        self.meetingConfig = getattr(self.tool, 'meeting-config-college')
        pmtmi.test_pm_UsedColorSystemShowColors(self)
        #we do the test for the council config
        self.meetingConfig = getattr(self.tool, 'meeting-config-council')
        pmtmi.test_pm_UsedColorSystemShowColors(self)

    def test_subproduct_call_SendItemToOtherMC(self):
        '''Test the send an item to another meetingConfig functionnality'''
        #we do the test for the college config, to send an item to the council
        self.meetingConfig = getattr(self.tool, 'meeting-config-college')
        pmtmi.test_pm_SendItemToOtherMC(self)

    def test_subproduct_call_SelectableCategories(self):
        '''Categories are available if isSelectable returns True.  By default,
           isSelectable will return active categories for wich intersection
           between MeetingCategory.usingGroups and current member
           proposingGroups is not empty.'''
        #we do the test for the council config
        self.meetingConfig = getattr(self.tool, 'meeting-config-council')
        self.meetingConfig.useGroupsAsCategories = False
        pmtmi.test_pm_SelectableCategories(self)

    def test_subproduct_call_AddAutoCopyGroups(self):
        '''Test the functionnality of automatically adding some copyGroups depending on
           the TAL expression defined on every MeetingGroup.asCopyGroupOn.'''
        pmtmi.test_pm_AddAutoCopyGroups(self)

    def test_subproduct_call_UpdateAdvices(self):
        '''See doc string in PloneMeeting.'''
        pmtmi.test_pm_UpdateAdvices(self)

    def test_subproduct_call_SendItemToOtherMCWithAnnexes(self):
        '''See doc string in PloneMeeting.'''
        pmtmi.test_pm_SendItemToOtherMCWithAnnexes(self)

    def test_subproduct_call_CopyGroups(self):
        '''See doc string in PloneMeeting.'''
        pmtmi.test_pm_CopyGroups(self)

    def test_subproduct_call_PowerObserversGroups(self):
        '''See doc string in PloneMeeting.'''
        pmtmi.test_pm_PowerObserversGroups(self)

    def test_subproduct_call_ItemIsSigned(self):
        '''See doc string in PloneMeeting.'''
        pmtmi.test_pm_ItemIsSigned(self)

    def test_subproduct_call_IsPrivacyViewable(self):
        '''See doc string in PloneMeeting.'''
        # use self.meetingConfig2 that has a 'published' state
        self.meetingConfig = self.meetingConfig2
        pmtmi.test_pm_IsPrivacyViewable(self)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    # launch only tests prefixed by 'test_mc_' to avoid launching the tests coming from pmtmi
    suite.addTest(makeSuite(testMeetingItem, prefix='test_subproduct_'))
    return suite
