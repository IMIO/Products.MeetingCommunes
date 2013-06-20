# -*- coding: utf-8 -*-
#
# File: testAdvices.py
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
from Products.PloneMeeting.tests.testAdvices import testAdvices as pmta


class testAdvices(MeetingCommunesTestCase, pmta):
    '''Tests various aspects of advices management.
       Advices are enabled for PloneGov Assembly, not for PloneMeeting Assembly.'''

    def test_subproduct_call_ViewItemToAdvice(self):
        '''Run the testViewItemToAdvice from PloneMeeting.'''
        pmta.test_pm_ViewItemToAdvice(self)

    def test_subproduct_call_AddEditDeleteAdvices(self):
        '''Run the testAddEditDeleteAdvices from PloneMeeting.'''
        pmta.test_pm_AddEditDeleteAdvices(self)

    def test_subproduct_call_GiveAdviceOnCreatedItem(self):
        '''Run the testGiveAdviceOnCreatedItem from PloneMeeting.'''
        pmta.test_pm_GiveAdviceOnCreatedItem(self)

    def test_subproduct_call_AdvicesInvalidation(self):
        '''Run the testAdvicesInvalidation from PloneMeeting.'''
        pmta.test_pm_AdvicesInvalidation(self)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testAdvices, prefix='test_subproduct_'))
    return suite
