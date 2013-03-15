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

    def test_mc_VerifyTestNumbers(self):
        """
            We verify that there are the same test methods in original product and this sub-product
        """
        tpm = self.getTestMethods(pmtmi, 'test')
        tmc = self.getTestMethods(testMeetingItem, 'test_mc_call_')
        missing = []
        for key in tpm:
            key2 = key.replace('test', 'test_mc_call_')
            if not key2 in tmc:
                missing.append(key)
        if len(missing):
            self.fail("missing test methods %s from PloneMeeting test class '%s'" % (missing, 'testMeetingItem'))

    def test_mc_call_ListProposingGroup(self):
        """
           Run the testListProposingGroup from PloneMeeting
        """
        #we do the test for the college config
        self.meetingConfig = getattr(self.tool, 'meeting-config-college')
        pmtmi.testListProposingGroup(self)
        #we do the test for the council config
        self.meetingConfig = getattr(self.tool, 'meeting-config-council')
        pmtmi.testListProposingGroup(self)

    def test_mc_call_UsedColorSystemGetColoredLink(self):
        """
           Test the selected system of color while getting a colored link
        """
        #we do the test for the college config
        self.meetingConfig = getattr(self.tool, 'meeting-config-college')
        pmtmi.testUsedColorSystemGetColoredLink(self)
        #we do the test for the council config
        self.meetingConfig = getattr(self.tool, 'meeting-config-council')
        pmtmi.testUsedColorSystemGetColoredLink(self)

    def test_mc_call_UsedColorSystemShowColors(self):
        """
           Test the selected system of color
        """
        #we do the test for the college config
        self.meetingConfig = getattr(self.tool, 'meeting-config-college')
        pmtmi.testUsedColorSystemShowColors(self)
        #we do the test for the council config
        self.meetingConfig = getattr(self.tool, 'meeting-config-council')
        pmtmi.testUsedColorSystemShowColors(self)

    def test_mc_call_SendItemToOtherMC(self):
        '''Test the send an item to another meetingConfig functionnality'''
        #we do the test for the college config, to send an item to the council
        self.meetingConfig = getattr(self.tool, 'meeting-config-college')
        self._adaptCategoriesForTest(self.meetingConfig)
        pmtmi.testSendItemToOtherMC(self)

    def test_mc_call_SelectableCategories(self):
        '''Categories are available if isSelectable returns True.  By default,
           isSelectable will return active categories for wich intersection
           between MeetingCategory.usingGroups and current member
           proposingGroups is not empty.'''
        #we do the test for the council config
        self.meetingConfig = getattr(self.tool, 'meeting-config-council')
        self.meetingConfig.useGroupsAsCategories = False
        self._adaptCategoriesForTest(self.meetingConfig)
        pmtmi.testSelectableCategories(self)

    def _getNecessaryMeetingTransitionsToAcceptItem(self):
        '''Returns the necessary transitions to trigger on the Meeting before being
           able to accept an item.'''
        return ['freeze', 'decide', ]

    def test_mc_call_AddAutoCopyGroups(self):
        '''Test the functionnality of automatically adding some copyGroups depending on
           the TAL expression defined on every MeetingGroup.asCopyGroupOn.'''
        pmtmi.testAddAutoCopyGroups(self)

    def test_mc_call_UpdateAdvices(self):
        '''See doc string in PloneMeeting.'''
        pmtmi.testUpdateAdvices(self)

    def test_mc_call_SendItemToOtherMCWithAnnexes(self):
        '''See doc string in PloneMeeting.'''
        pmtmi.testSendItemToOtherMCWithAnnexes(self)

    def test_mc_call_CopyGroups(self):
        '''See doc string in PloneMeeting.'''
        pmtmi.testCopyGroups(self)

    def test_mc_call_PowerObserversGroups(self):
        '''See doc string in PloneMeeting.'''
        pmtmi.testPowerObserversGroups(self)

    def test_mc_call_ItemIsSigned(self):
        '''Test the functionnality around MeetingItem.itemIsSigned field.'''
        mtool = getToolByName(self.portal, 'portal_membership')
        authMember = mtool.getAuthenticatedMember
        login(self.portal, 'pmCreator1')
        item = self.create('MeetingItem')
        item.setCategory('development')
        item.setDecision('<p>My decision</p>', mimetype='text/html')
        # MeetingMember can not setItemIsSigned
        self.assertEquals(item.maySignItem(authMember()), False)
        self.assertRaises(Unauthorized, item.setItemIsSigned, True)
        self.assertRaises(Unauthorized, item.restrictedTraverse('@@toggle_item_is_signed'), item.UID())
        # MeetingManagers neither, the item must be decided...
        self.changeUser('pmManager')
        self.assertRaises(Unauthorized, item.setItemIsSigned, True)
        self.assertRaises(Unauthorized, item.restrictedTraverse('@@toggle_item_is_signed'), item.UID())
        meetingDate = DateTime('2008/06/12 08:00:00')
        meeting = self.create('Meeting', date=meetingDate)
        self.changeUser('pmCreator1')
        self.do(item, 'propose')
        self.changeUser('pmReviewer1')
        self.do(item, 'validate')
        self.changeUser('pmManager')
        self.do(item, 'present')
        self.assertEquals(item.maySignItem(authMember()), False)
        self.assertRaises(Unauthorized, item.setItemIsSigned, True)
        self.assertRaises(Unauthorized, item.restrictedTraverse('@@toggle_item_is_signed'), item.UID())
        self.do(meeting, 'freeze')
        self.assertEquals(item.maySignItem(authMember()), False)
        self.assertRaises(Unauthorized, item.setItemIsSigned, True)
        self.assertRaises(Unauthorized, item.restrictedTraverse('@@toggle_item_is_signed'), item.UID())
        self.do(meeting, 'decide')
        self.assertEquals(item.maySignItem(authMember()), False)
        self.assertRaises(Unauthorized, item.setItemIsSigned, True)
        self.assertRaises(Unauthorized, item.restrictedTraverse('@@toggle_item_is_signed'), item.UID())
        # now accept the item so MeetingManagers can sign it
        self.do(item, 'accept')
        self.assertEquals(item.maySignItem(authMember()), True)
        item.setItemIsSigned(True)
        # a signed item can still be unsigned until the meeting is closed
        self.assertEquals(item.maySignItem(authMember()), True)
        # call to @@toggle_item_is_signed will set it back to False (toggle)
        item.restrictedTraverse('@@toggle_item_is_signed')(item.UID())
        self.assertEquals(item.getItemIsSigned(), False)
        # toggle itemIsSigned value again
        item.restrictedTraverse('@@toggle_item_is_signed')(item.UID())
        self.assertEquals(item.getItemIsSigned(), True)
        # check accessing setItemIsSigned directly
        item.setItemIsSigned(False)
        self.do(meeting, 'close')
        # still able to sign an unsigned item in a closed meeting
        self.assertEquals(item.maySignItem(authMember()), True)
        # once signed in a closed/archived meeting, no more able to unsign the item
        item.setItemIsSigned(True)
        self.assertEquals(item.maySignItem(authMember()), False)
        self.assertRaises(Unauthorized, item.setItemIsSigned, False)
        self.assertRaises(Unauthorized, item.restrictedTraverse('@@toggle_item_is_signed'), item.UID())


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    # launch only tests prefixed by 'test_mc_' to avoid launching the tests coming from pmtmi
    suite.addTest(makeSuite(testMeetingItem, prefix='test_mc_'))
    return suite
