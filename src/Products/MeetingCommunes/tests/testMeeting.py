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
        """Run the test_pm_InsertItem from PloneMeeting.
           See docstring in PloneMeeting."""
        self.test_pm_InsertItem()

    def test_subproduct_call_InsertItemOnProposingGroupsWithDisabledGroup(self):
        """Run the test_pm_InsertItemOnProposingGroupsWithDisabledGroup from PloneMeeting.
           See docstring in PloneMeeting."""
        self.test_pm_InsertItemOnProposingGroupsWithDisabledGroup()

    def test_subproduct_call_InsertItemCategories(self):
        """Run the test_pm_InsertItemCategories from PloneMeeting.
           See docstring in PloneMeeting."""
        self.test_pm_InsertItemCategories()

    def test_subproduct_call_InsertItemOnCategoriesWithDisabledCategory(self):
        """Run the test_pm_InsertItemOnCategoriesWithDisabledCategory from PloneMeeting.
           See docstring in PloneMeeting."""
        self.test_pm_InsertItemOnCategoriesWithDisabledCategory()

    def test_subproduct_call_InsertItemAllGroups(self):
        """Run the test_pm_InsertItemAllGroups from PloneMeeting.
           See docstring in PloneMeeting."""
        self.test_pm_InsertItemAllGroups()

    def test_subproduct_call_InsertItemOnAllGroupsWithDisabledGroup(self):
        """Run the test_pm_InsertItemOnAllGroupsWithDisabledGroup from PloneMeeting.
           See docstring in PloneMeeting."""
        self.test_pm_InsertItemOnAllGroupsWithDisabledGroup()

    def test_subproduct_call_InsertItemPrivacyThenProposingGroups(self):
        """Run the test_pm_InsertItemPrivacyThenProposingGroups from PloneMeeting.
           See docstring in PloneMeeting."""
        self.test_pm_InsertItemPrivacyThenProposingGroups()

    def test_subproduct_call_InsertItemPrivacyThenProposingGroupsWithDisabledGroup(self):
        """Run the test_pm_InsertItemPrivacyThenProposingGroupsWithDisabledGroup from PloneMeeting.
           See docstring in PloneMeeting."""
        self.test_pm_InsertItemPrivacyThenProposingGroupsWithDisabledGroup()

    def test_subproduct_call_InsertItemPrivacyThenCategories(self):
        """Run the test_pm_InsertItemPrivacyThenCategories from PloneMeeting.
           See docstring in PloneMeeting."""
        self.test_pm_InsertItemPrivacyThenCategories()

    def test_subproduct_call_InsertItemPrivacyThenCategoriesWithDisabledCategory(self):
        """Run the test_pm_InsertItemPrivacyThenCategoriesWithDisabledCategory from PloneMeeting.
           See docstring in PloneMeeting."""
        self.test_pm_InsertItemPrivacyThenCategoriesWithDisabledCategory()

    def test_subproduct_call_RemoveOrDeleteLinkedItem(self):
        """Run the test_pm_RemoveOrDeleteLinkedItem from PloneMeeting.
           See docstring in PloneMeeting."""
        self.test_pm_RemoveOrDeleteLinkedItem()

    def test_subproduct_call_MeetingNumbers(self):
        """Run the test_pm_MeetingNumbers from PloneMeeting.
           See docstring in PloneMeeting."""
        self.test_pm_MeetingNumbers()

    def test_subproduct_call_AvailableItems(self):
        """Run the test_pm_AvailableItems from PloneMeeting.
           See docstring in PloneMeeting."""
        self.test_pm_AvailableItems()

    def test_subproduct_call_PresentSeveralItems(self):
        """Run the testPresentSeveralItems from PloneMeeting.
           See docstring in PloneMeeting."""
        self.test_pm_PresentSeveralItems()

    def test_subproduct_call_DecideSeveralItems(self):
        """Run the testDecideSeveralItems from PloneMeeting."""
        self.test_pm_DecideSeveralItems()

    def test_subproduct_call_Validate_date(self):
        """Run the test_pm_validate_date from PloneMeeting."""
        self.test_pm_Validate_date()

    def test_subproduct_call_InsertItemOnCategoriesThenOnToOtherMCToCloneTo(self):
        """Run the test_pm_InsertItemOnCategoriesThenOnToOtherMCToCloneTo from PloneMeeting."""
        self.test_pm_InsertItemOnCategoriesThenOnToOtherMCToCloneTo()

    def test_subproduct_call_InsertItemOnToDiscuss(self):
        """Run the test_pm_InsertItemOnToDiscuss from PloneMeeting."""
        self.test_pm_InsertItemOnToDiscuss()

    def test_subproduct_call_InsertItemByCategoriesThenProposingGroups(self):
        """Run the test_pm_InsertItemByCategoriesThenProposingGroups from PloneMeeting."""
        self.test_pm_InsertItemByCategoriesThenProposingGroups()

    def test_subproduct_call_InsertItemOnToOtherMCToCloneTo(self):
        """Run the test_pm_InsertItemOnToOtherMCToCloneTo from PloneMeeting."""
        self.test_pm_InsertItemOnToOtherMCToCloneTo()

    def test_subproduct_call_InsertItemInToDiscussThenProposingGroup(self):
        """Run the test_pm_InsertItemInToDiscussThenProposingGroup from PloneMeeting."""
        self.test_pm_InsertItemInToDiscussThenProposingGroup()

    def test_subproduct_call_TitleAndPlaceCorrectlyUpdatedOnEdit(self):
        """Run the test_pm_TitleAndPlaceCorrectlyUpdatedOnEdit from PloneMeeting."""
        self.test_pm_TitleAndPlaceCorrectlyUpdatedOnEdit()

    def test_subproduct_call_NumberOfItems(self):
        """Run the test_pm_NumberOfItems from PloneMeeting."""
        self.test_pm_NumberOfItems()

    def test_subproduct_call_PresentItemToMeeting(self):
        """Run the test_pm_PresentItemToMeeting from PloneMeeting."""
        self.test_pm_PresentItemToMeeting()

    def test_subproduct_call_Validate_place(self):
        """Run the test_pm_Validate_place from PloneMeeting."""
        self.test_pm_Validate_place()

    def test_subproduct_call_GetItemByNumber(self):
        """Run the test_pm_GetItemByNumber from PloneMeeting."""
        self.test_pm_GetItemByNumber()

    def test_subproduct_call_GetItemsInOrder(self):
        """Run the test_pm_GetItemsInOrder from PloneMeeting."""
        self.test_pm_GetItemsInOrder()

    def test_subproduct_call_RemoveSeveralItems(self):
        """Run the test_pm_RemoveSeveralItems from PloneMeeting."""
        self.test_pm_RemoveSeveralItems()

    def test_subproduct_call_RemoveWholeMeeting(self):
        """Run the test_pm_RemoveWholeMeeting from PloneMeeting."""
        self.test_pm_RemoveWholeMeeting()

    def test_subproduct_call_DeletingMeetingUpdateItemsPreferredMeeting(self):
        """Run the test_pm_DeletingMeetingUpdateItemsPreferredMeeting from PloneMeeting."""
        self.test_pm_DeletingMeetingUpdateItemsPreferredMeeting()


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    # launch only tests prefixed by 'test_subproduct_' to avoid launching the tests coming from pmtm
    suite.addTest(makeSuite(testMeeting, prefix='test_subproduct_'))
    return suite
