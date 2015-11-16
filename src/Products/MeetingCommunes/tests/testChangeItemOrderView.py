# -*- coding: utf-8 -*-
#
# File: testChangeItemOrderView.py
#
# Copyright (c) 2013 by Imio.be
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
from Products.PloneMeeting.tests.testChangeItemOrderView import testChangeItemOrderView as pmciov


class testChangeItemOrderView(MeetingCommunesTestCase, pmciov):
    '''Tests the ChangeItemOrderView class methods.'''

    def test_subproduct_call_ChangeItemOrderMoveUpDown(self):
        '''Check docstring in PloneMeeting.'''
        self.test_pm_ChangeItemOrderMoveUpDown()

    def test_subproduct_call_ChangeItemOrderMoveUpDownWithSubnumbers(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_ChangeItemOrderMoveUpDownWithSubnumbers()

    def test_subproduct_call_ChangeItemOrderMoveAtGivenNumber(self):
        '''Check docstring in PloneMeeting.'''
        self.test_pm_ChangeItemOrderMoveAtGivenNumber()

    def test_subproduct_call_MoveLateItemDoNotChangeNormalItems(self):
        '''Check docstring in PloneMeeting.'''
        self.test_pm_MoveLateItemDoNotChangeNormalItems()

    def test_subproduct_call_MayChangeItemOrder(self):
        '''Check docstring in PloneMeeting.'''
        self.test_pm_MayChangeItemOrder()

    def test_subproduct_call_ChangeItemOrderMoveIntegerToInteger(self):
        '''Check docstring in PloneMeeting.'''
        self.test_pm_ChangeItemOrderMoveIntegerToInteger()

    def test_subproduct_call_ChangeItemOrderMoveSubnumberToInteger(self):
        '''Check docstring in PloneMeeting.'''
        self.test_pm_ChangeItemOrderMoveSubnumberToInteger()

    def test_subproduct_call_ChangeItemOrderMoveSubnumberToSubnumber(self):
        '''Check docstring in PloneMeeting.'''
        self.test_pm_ChangeItemOrderMoveSubnumberToSubnumber()

    def test_subproduct_call_ChangeItemOrderMoveUpToFirstPositionWithSubnumbers(self):
        '''Check docstring in PloneMeeting.'''
        self.test_pm_ChangeItemOrderMoveUpToFirstPositionWithSubnumbers()

    def test_subproduct_call_ChangeItemOrderMoveOutFromSubnumber(self):
        '''Check docstring in PloneMeeting.'''
        self.test_pm_ChangeItemOrderMoveOutFromSubnumber()

    def test_subproduct_call_ChangeItemOrderMoveIntegerToSubnumber(self):
        '''Check docstring in PloneMeeting.'''
        self.test_pm_ChangeItemOrderMoveIntegerToSubnumber()

    def test_subproduct_call_ChanteItemOrderSetup(self):
        '''Check docstring in PloneMeeting.'''
        self.test_pm_ChanteItemOrderSetup()


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testChangeItemOrderView, prefix='test_subproduct_'))
    return suite
