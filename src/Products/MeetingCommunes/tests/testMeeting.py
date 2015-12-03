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

from Products.MeetingCommunes.tests.MeetingCommunesTestCase import MeetingCommunesTestCase
from Products.PloneMeeting.tests.testMeeting import testMeeting as pmtm


class testMeeting(MeetingCommunesTestCase, pmtm):
    """
        Tests the Meeting class methods.
    """

    def test_subproduct_call_InsertItem(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_InsertItem()

    def test_subproduct_call_InsertItemOnProposingGroupsWithDisabledGroup(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_InsertItemOnProposingGroupsWithDisabledGroup()

    def test_subproduct_call_InsertItemCategories(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_InsertItemCategories()

    def test_subproduct_call_InsertItemOnCategoriesWithDisabledCategory(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_InsertItemOnCategoriesWithDisabledCategory()

    def test_subproduct_call_InsertItemAllGroups(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_InsertItemAllGroups()

    def test_subproduct_call_InsertItemOnAllGroupsWithDisabledGroup(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_InsertItemOnAllGroupsWithDisabledGroup()

    def test_subproduct_call_InsertItemWithSubNumbers(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_InsertItemWithSubNumbers()

    def test_subproduct_call_InsertItemPrivacyThenProposingGroups(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_InsertItemPrivacyThenProposingGroups()

    def test_subproduct_call_InsertItemPrivacyThenProposingGroupsWithDisabledGroup(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_InsertItemPrivacyThenProposingGroupsWithDisabledGroup()

    def test_subproduct_call_InsertItemPrivacyThenCategories(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_InsertItemPrivacyThenCategories()

    def test_subproduct_call_InsertItemPrivacyThenCategoriesWithDisabledCategory(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_InsertItemPrivacyThenCategoriesWithDisabledCategory()

    def test_subproduct_call_RemoveOrDeleteLinkedItem(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_RemoveOrDeleteLinkedItem()

    def test_subproduct_call_RemoveItemWithSubnumbers(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_RemoveItemWithSubnumbers()

    def test_subproduct_call_RemoveItemWithSubnumbersRemovedItemBeforeSubnumbers(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_RemoveItemWithSubnumbersRemovedItemBeforeSubnumbers()

    def test_subproduct_call_MeetingNumbers(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_MeetingNumbers()

    def test_subproduct_call_AvailableItems(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_AvailableItems()

    def test_subproduct_call_PresentSeveralItems(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_PresentSeveralItems()

    def test_subproduct_call_PresentSeveralItemsWithAutoSendToOtherMCUntilPresented(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_PresentSeveralItemsWithAutoSendToOtherMCUntilPresented()

    def test_subproduct_call_DecideSeveralItems(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_DecideSeveralItems()

    def test_subproduct_call_Validate_date(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_Validate_date()

    def test_subproduct_call_InsertItemOnCategoriesThenOnToOtherMCToCloneTo(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_InsertItemOnCategoriesThenOnToOtherMCToCloneTo()

    def test_subproduct_call_InsertItemOnToDiscuss(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_InsertItemOnToDiscuss()

    def test_subproduct_call_InsertItemByCategoriesThenProposingGroups(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_InsertItemByCategoriesThenProposingGroups()

    def test_subproduct_call_InsertItemOnToOtherMCToCloneTo(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_InsertItemOnToOtherMCToCloneTo()

    def test_subproduct_call_InsertItemInToDiscussThenProposingGroup(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_InsertItemInToDiscussThenProposingGroup()

    def test_subproduct_call_TitleAndPlaceCorrectlyUpdatedOnEdit(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_TitleAndPlaceCorrectlyUpdatedOnEdit()

    def test_subproduct_call_NumberOfItems(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_NumberOfItems()

    def test_subproduct_call_PresentItemToMeeting(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_PresentItemToMeeting()

    def test_subproduct_call_Validate_place(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_Validate_place()

    def test_subproduct_call_GetItemByNumber(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_GetItemByNumber()

    def test_subproduct_call_GetItems(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_GetItems()

    def test_subproduct_call_RemoveSeveralItems(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_RemoveSeveralItems()

    def test_subproduct_call_RemoveWholeMeeting(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_RemoveWholeMeeting()

    def test_subproduct_call_DeletingMeetingUpdateItemsPreferredMeeting(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_DeletingMeetingUpdateItemsPreferredMeeting()

    def test_subproduct_call_MeetingActionsPanelCaching(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_MeetingActionsPanelCaching()

    def test_subproduct_call_InsertItemOnListTypeThenProposingGroup(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_InsertItemOnListTypeThenProposingGroup()

    def test_subproduct_call_InsertItemOnListTypes(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_InsertItemOnListTypes()

    def test_subproduct_call_GetNextMeeting(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_GetNextMeeting()

    def test_subproduct_call_GetPreviousMeeting(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_GetPreviousMeeting()

    def test_subproduct_call_MeetingStrikedAssembly(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_MeetingStrikedAssembly()

    def test_subproduct_call_ChaningMeetingDateUpdateLinkedItemsMeetingDateMetadata(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_ChaningMeetingDateUpdateLinkedItemsMeetingDateMetadata()

    def test_subproduct_call_GetFirstItemNumberIgnoresSubnumbers(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_GetFirstItemNumberIgnoresSubnumbers()


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    # launch only tests prefixed by 'test_subproduct_' to avoid launching the tests coming from pmtm
    suite.addTest(makeSuite(testMeeting, prefix='test_subproduct_'))
    return suite
