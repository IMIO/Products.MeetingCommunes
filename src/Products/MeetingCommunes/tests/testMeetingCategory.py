# -*- coding: utf-8 -*-
#
# File: testMeetingCategory.py
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

from plone.app.testing import logout
from Products.MeetingCommunes.tests.MeetingCommunesTestCase import \
    MeetingCommunesTestCase
from Products.PloneMeeting.tests.testMeetingCategory import testMeetingCategory as pmmc


class testMeetingCategory(MeetingCommunesTestCase, pmmc):
    '''Tests the MeetingCategory class methods.'''

    def test_subproduct_call_CanNotRemoveLinkedMeetingCategory(self):
        '''Run the test_pm_CanNotRemoveLinkedMeetingCategory from PloneMeeting.'''
        # remove every items in the metingConfig that are using the 'developers' group
        self.changeUser('admin')
        self.meetingConfig.recurringitems.manage_delObjects(
            [item.getId() for item in (self.meetingConfig.getItems() + self.meetingConfig.getItems('as_template_item'))
             if item.getProposingGroup() == 'developers'])
        logout()
        self.test_pm_CanNotRemoveLinkedMeetingCategory()


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testMeetingCategory, prefix='test_subproduct_'))
    return suite
