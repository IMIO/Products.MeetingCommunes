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

from plone.app.testing import logout
from Products.MeetingCommunes.tests.MeetingCommunesTestCase import \
    MeetingCommunesTestCase
from Products.PloneMeeting.tests.testMeetingCategory import testMeetingCategory as pmmc


class testMeetingCategory(MeetingCommunesTestCase, pmmc):
    '''Tests the MeetingCategory class methods.'''

    def test_mc_VerifyTestNumbers(self):
        """
            We verify that there are the same test methods in original product and this sub-product
        """
        tpm = self.getTestMethods(pmmc, 'test')
        tmc = self.getTestMethods(testMeetingCategory, 'test_mc_call_')
        missing = []
        for key in tpm:
            key2 = key.replace('test', 'test_mc_call_')
            if not key2 in tmc:
                missing.append(key)
        if len(missing):
            self.fail("missing test methods %s from PloneMeeting test class '%s'" % (missing, 'testMeetingCategory'))

    def test_mc_call_CanNotRemoveLinkedMeetingCategory(self):
        '''Run the testCanNotRemoveLinkedMeetingCategory from PloneMeeting.'''
        # remove every recurring items before launching the test
        self.changeUser('admin')
        self.meetingConfig.recurringitems.manage_delObjects([item.getId() for item in self.meetingConfig.getItems()])
        logout()
        self.testCanNotRemoveLinkedMeetingCategory()


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testMeetingCategory, prefix='test_mc_'))
    return suite
