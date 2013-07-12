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

from Products.MeetingCommunes.tests.MeetingCommunesTestCase import \
    MeetingCommunesTestCase
from Products.PloneMeeting.tests.testMeeting import testMeeting as pmtm


class testMeeting(MeetingCommunesTestCase, pmtm):
    """
        Tests the Meeting class methods.
    """

    def test_subproduct_call_InsertItem(self):
        """Run the test_pm_InsertItem from PloneMeeting."""
        self.test_pm_InsertItem()

    def test_subproduct_call_InsertItemCategories(self):
        """Run the test_pm_InsertItemCategories from PloneMeeting."""
        self.test_pm_InsertItemCategories()

    def test_subproduct_call_InsertItemAllGroups(self):
        """Run the test_pm_InsertItemAllGroups from PloneMeeting."""
        self.test_pm_InsertItemAllGroups()

    def test_subproduct_call_InsertItemPrivacyThenProposingGroups(self):
        """Run the test_pm_InsertItemPrivacyThenProposingGroups from PloneMeeting."""
        self.test_pm_InsertItemPrivacyThenProposingGroups()

    def test_subproduct_call_InsertItemPrivacyThenCategories(self):
        """Run the test_pm_InsertItemPrivacyThenCategories from PloneMeeting."""
        self.test_pm_InsertItemPrivacyThenCategories()

    def test_subproduct_call_RemoveOrDeleteLinkedItem(self):
        """Run the test_pm_RemoveOrDeleteLinkedItem from PloneMeeting."""
        self.test_pm_RemoveOrDeleteLinkedItem()

    def test_subproduct_call_MeetingNumbers(self):
        """Run the test_pm_MeetingNumbers from PloneMeeting."""
        self.test_pm_MeetingNumbers()

    def test_subproduct_call_AvailableItems(self):
        """Run the testAvailableItems from PloneMeeting."""
        self.test_pm_AvailableItems()

    def test_subproduct_call_PresentSeveralItems(self):
        """
          Run the testPresentSeveralItems from PloneMeeting
        """
        self.test_pm_PresentSeveralItems()

    def test_subproduct_call_DecideSeveralItems(self):
        """
          Run the testDecideSeveralItems from PloneMeeting
        """
        self.test_pm_DecideSeveralItems()


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    # launch only tests prefixed by 'test_subproduct_' to avoid launching the tests coming from pmtm
    suite.addTest(makeSuite(testMeeting, prefix='test_subproduct_'))
    return suite
