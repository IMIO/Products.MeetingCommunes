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
from Products.PloneMeeting.tests.testMeetingFile import testMeetingFile as pmmf


class testMeetingFile(MeetingCommunesTestCase, pmmf):
    '''Tests the MeetingFile class methods.'''

    def test_subproduct_call_MayChangeToPrint(self):
        '''Run the test_pm_MayChangeToPrint from PloneMeeting.'''
        self.test_pm_MayChangeToPrint()

    def test_subproduct_call_MayChangeConfidentiality(self):
        '''Run the test_pm_MayChangeConfidentiality from PloneMeeting.'''
        self.test_pm_MayChangeConfidentiality()

    def test_subproduct_call_MeetingFileFoundInItemSearchableText(self):
        '''Run the test_pm_MeetingFileFoundInItemSearchableText from PloneMeeting.'''
        self.test_pm_MeetingFileFoundInItemSearchableText()


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testMeetingFile, prefix='test_subproduct_'))
    return suite
