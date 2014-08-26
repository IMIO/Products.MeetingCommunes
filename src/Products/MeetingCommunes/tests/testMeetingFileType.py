# -*- coding: utf-8 -*-
#
# File: testMeetingFileType.py
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
from Products.PloneMeeting.tests.testMeetingFileType import testMeetingFileType as pmmft


class testMeetingFileType(MeetingCommunesTestCase, pmmft):
    '''Tests the MeetingFileType class methods.'''

    def test_subproduct_call_CanNotRemoveLinkedMeetingFileType(self):
        '''Run the testCanNotRemoveLinkedMeetingFileType from PloneMeeting.'''
        self.test_pm_CanNotRemoveLinkedMeetingFileType()

    def test_subproduct_call_CanNotRemoveLinkedSubMeetingFileType(self):
        '''Run the testCanNotRemoveLinkedSubMeetingFileType from PloneMeeting.'''
        self.test_pm_CanNotRemoveLinkedSubMeetingFileType()

    def test_subproduct_call_CanNotChangeRelatedToOfUsedMeetingFileType(self):
        '''Run the test_pm_CanNotChangeRelatedToOfUsedMeetingFileType from PloneMeeting.'''
        self.test_pm_CanNotChangeRelatedToOfUsedMeetingFileType()

    def test_subproduct_call_validate_subTypes(self):
        '''Run the test_pm_validate_subTypes from PloneMeeting.'''
        self.test_pm_validate_subTypes()


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testMeetingFileType, prefix='test_subproduct_'))
    return suite
