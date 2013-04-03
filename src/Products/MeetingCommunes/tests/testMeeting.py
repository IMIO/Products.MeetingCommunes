# -*- coding: utf-8 -*-
#
# File: testMeeting.py
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

from plone.app.testing import login
from Products.MeetingCommunes.tests.MeetingCommunesTestCase import \
    MeetingCommunesTestCase
from Products.PloneMeeting.tests.testMeeting import testMeeting as pmtm


class testMeeting(MeetingCommunesTestCase, pmtm):
    """
        Tests the Meeting class methods.
    """

    def test_mc_VerifyTestNumbers(self):
        """
            We verify that there are the same test methods in original product and this sub-product
        """
        tpm = self.getTestMethods(pmtm, 'test')
        tmc = self.getTestMethods(testMeeting, 'test_mc_call_')
        missing = []
        for key in tpm:
            key2 = key.replace('test', 'test_mc_call_')
            if not key2 in tmc:
                missing.append(key)
        if len(missing):
            self.fail("missing test methods %s from PloneMeeting test class '%s'" % (missing, 'testMeeting'))

    def test_mc_call_InsertItem(self):
        """
          Run the testInsertItem from PloneMeeting
          We can not call it here...
          Write it and adapt it here...
        """
        #depending on order of insertion and recurring item,s the result is different
        #between college and council
        login(self.portal, 'pmManager')
        for meetingConfig in self.tool.getActiveConfigs():
            meetingConfigId = meetingConfig.getId()
            self.setMeetingConfig(meetingConfigId)
            meeting = self._createMeetingWithItems()
            if meetingConfigId == 'meeting-config-council':
                #here, we have recurring items
                expected = ['recItem1', 'o3', 'o5', 'o2', 'o4', 'o6']
            if meetingConfigId == 'meeting-config-college':
                #here, we have recurring items
                expected = ['recurringagenda1',
                            'recurringofficialreport1',
                            'recurringofficialreport2',
                            'o2',
                            'o3',
                            'o4',
                            'o5',
                            'o6', ]
            self.assertEquals([item.id for item in meeting.getItemsInOrder()],
                              expected)

    def test_mc_call_InsertItemCategories(self):
        '''Sort method tested here is "on_categories".'''
        login(self.portal, 'pmManager')
        for meetingConfig in self.tool.getActiveConfigs():
            meetingConfigId = meetingConfig.getId()
            self.setMeetingConfig(meetingConfigId)
            self.meetingConfig.setSortingMethodOnAddItem('on_categories')
            self.meetingConfig.setUseGroupsAsCategories(False)
            self._adaptCategoriesForTest(self.meetingConfig)
            meeting = self._createMeetingWithItems()
            if meetingConfigId == 'meeting-config-council':
                #here, we have recurring items
                expected = ['recItem1', 'o3', 'o4', 'o5', 'o6', 'o2']
            if meetingConfigId == 'meeting-config-college':
                #here, we have recurring items
                expected = ['recurringagenda1',
                            'recurringofficialreport1',
                            'recurringofficialreport2',
                            'o3',
                            'o4',
                            'o5',
                            'o6',
                            'o2']
            self.assertEquals([item.id for item in meeting.getItemsInOrder()],
                              expected)

    def test_mc_call_InsertItemAllGroups(self):
        """
           Run the testInsertItemAllGroups from PloneMeeting
        """
        #we do the test for the college config
        login(self.portal, 'pmManager')
        for meetingConfig in ('meeting-config-college', 'meeting-config-council', ):
            self.setMeetingConfig(meetingConfig)
            self.meetingConfig.setSortingMethodOnAddItem('on_all_groups')
            meeting = self._createMeetingWithItems()
            if meetingConfig == 'meeting-config-council':
                #here, we have recurring items
                expected = ['recItem1', 'o3', 'o5', 'o2', 'o4', 'o6']
            if meetingConfig == 'meeting-config-college':
                #here, we have recurring items
                expected = ['recurringagenda1',
                            'recurringofficialreport1',
                            'recurringofficialreport2',
                            'o3',
                            'o5',
                            'o2',
                            'o4',
                            'o6']
            self.assertEquals([item.id for item in meeting.getItemsInOrder()],
                              expected)

    def test_mc_call_InsertItemPrivacyThenProposingGroups(self):
        '''Sort method tested here is "on_privacy_then_proposing_groups".'''
        #we do the test for the college config
        login(self.portal, 'pmManager')
        for meetingConfig in ('meeting-config-college', 'meeting-config-council', ):
            self.setMeetingConfig(meetingConfig)
            self.meetingConfig.setSortingMethodOnAddItem('on_privacy_then_proposing_groups')
            meeting = self._createMeetingWithItems()
            if meetingConfig == 'meeting-config-council':
                #here, we have recurring items
                expected = ['recItem1', 'o3', 'o2', 'o6', 'o5', 'o4']
            if meetingConfig == 'meeting-config-college':
                #here, we have recurring items
                expected = ['recurringagenda1',
                            'recurringofficialreport1',
                            'recurringofficialreport2',
                            'o3',
                            'o2',
                            'o6',
                            'o5',
                            'o4']
            self.assertEquals([item.id for item in meeting.getItemsInOrder()],
                              expected)

    def test_mc_call_InsertItemPrivacyThenCategories(self):
        '''Sort method tested here is "on_privacy_then_categories".'''
        login(self.portal, 'pmManager')
        for meetingConfig in ('meeting-config-college', 'meeting-config-council', ):
            self.setMeetingConfig(meetingConfig)
            self.meetingConfig.setSortingMethodOnAddItem('on_privacy_then_categories')
            self.meetingConfig.setUseGroupsAsCategories(False)
            # as we do not use groups as categories, but real categories, we have to adapt them...
            self._adaptCategoriesForTest(self.meetingConfig)
            meeting = self._createMeetingWithItems()
            if meetingConfig == 'meeting-config-council':
                #here, we have recurring items
                expected = ['recItem1', 'o3', 'o6', 'o2', 'o4', 'o5']
            if meetingConfig == 'meeting-config-college':
                #here, we have recurring items
                expected = ['recurringagenda1',
                            'recurringofficialreport1',
                            'recurringofficialreport2',
                            'o3',
                            'o6',
                            'o2',
                            'o4',
                            'o5']
            self.assertEquals([item.id for item in meeting.getItemsInOrder()],
                              expected)

    def test_mc_call_AvailableItems(self):
        """
           Run the testAvailableItems from PloneMeeting
        """
        #we do the test for the college config
        self.meetingConfig = getattr(self.tool, 'meeting-config-college')
        pmtm.testAvailableItems(self)
        #we do the test for the council config
        self.meetingConfig = getattr(self.tool, 'meeting-config-council')
        pmtm.testAvailableItems(self)

    def test_mc_call_RemoveOrDeleteLinkedItem(self):
        """
           Run the testRemoveOrDeleteLinkedItem from PloneMeeting
        """
        login(self.portal, 'pmManager')
        meeting = self._createMeetingWithItems()
        self.assertEquals([item.id for item in meeting.getItemsInOrder()],
                          ['recurringagenda1',
                           'recurringofficialreport1',
                           'recurringofficialreport2',
                           'o2',
                           'o3',
                           'o4',
                           'o5',
                           'o6'])
        #remove an item
        item5 = getattr(meeting, 'o5')
        meeting.removeItem(item5)
        self.assertEquals([item.id for item in meeting.getItemsInOrder()],
                          ['recurringagenda1',
                           'recurringofficialreport1',
                           'recurringofficialreport2',
                           'o2',
                           'o3',
                           'o4',
                           'o6'])
        #delete a linked item
        item4 = getattr(meeting, 'o4')
        meeting.restrictedTraverse('@@delete_givenuid')(item4.UID())
        self.assertEquals([item.id for item in meeting.getItemsInOrder()],
                          ['recurringagenda1',
                           'recurringofficialreport1',
                           'recurringofficialreport2',
                           'o2',
                           'o3',
                           'o6'])
        self.meetingConfig = getattr(self.tool, 'meeting-config-council')
        pmtm.testRemoveOrDeleteLinkedItem(self)

    def test_mc_call_MeetingNumbers(self):
        """
           Run the testMeetingNumbers from PloneMeeting
        """
        # here, the last item number is updated in the config in the doClose
        # not in the doPublish
        login(self.portal, 'pmManager')
        m1 = self._createMeetingWithItems()
        self.assertEquals(self.meetingConfig.getLastMeetingNumber(), 0)
        self.assertEquals(m1.getMeetingNumber(), -1)
        self.do(m1, 'freeze')
        self.do(m1, 'decide')
        self.do(m1, 'close')
        self.assertEquals(m1.getMeetingNumber(), 1)
        self.assertEquals(self.meetingConfig.getLastMeetingNumber(), 1)
        m2 = self._createMeetingWithItems()
        self.do(m2, 'freeze')
        self.do(m2, 'decide')
        self.do(m2, 'close')
        self.assertEquals(m2.getMeetingNumber(), 2)
        self.assertEquals(self.meetingConfig.getLastMeetingNumber(), 2)
        self.meetingConfig = getattr(self.tool, 'meeting-config-council')
        m1 = self._createMeetingWithItems()
        self.assertEquals(self.meetingConfig.getLastMeetingNumber(), 0)
        self.assertEquals(m1.getMeetingNumber(), -1)
        self.do(m1, 'freeze')
        self.do(m1, 'publish')
        self.do(m1, 'decide')
        self.do(m1, 'close')
        self.assertEquals(m1.getMeetingNumber(), 1)
        self.assertEquals(self.meetingConfig.getLastMeetingNumber(), 1)
        m2 = self._createMeetingWithItems()
        self.do(m2, 'freeze')
        self.do(m2, 'publish')
        self.do(m2, 'decide')
        self.do(m2, 'close')
        self.assertEquals(m2.getMeetingNumber(), 2)
        self.assertEquals(self.meetingConfig.getLastMeetingNumber(), 2)

    def test_mc_call_DecideSeveralItems(self):
        """
          Run the testDecideSeveralItems from PloneMeeting
        """
        self.testDecideSeveralItems()


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    # launch only tests prefixed by 'test_mc_' to avoid launching the tests coming from pmtm
    suite.addTest(makeSuite(testMeeting, prefix='test_mc_'))
    return suite
