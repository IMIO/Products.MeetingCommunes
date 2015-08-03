# -*- coding: utf-8 -*-
#
# File: testAnnexes.py
#
# Copyright (c) 2007-2015 by Imio.be
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
from Products.PloneMeeting.tests.testAnnexes import testAnnexes as pmta


class testAnnexes(MeetingCommunesTestCase, pmta):
    ''' '''

    def test_subproduct_call_GetLastInsertedAnnex(self):
        '''Run the test_pm_GetLastInsertedAnnex from PloneMeeting.'''
        pmta.test_pm_GetLastInsertedAnnex(self)

    def test_subproduct_call_GetAnnexesByType(self):
        '''Run the test_pm_GetAnnexesByType from PloneMeeting.'''
        pmta.test_pm_GetAnnexesByType(self)

    def test_subproduct_call_GetAnnexesByTypeAnnexConfidentiality(self):
        '''Run the test_pm_GetAnnexesByTypeAnnexConfidentiality from PloneMeeting.'''
        pmta.test_pm_GetAnnexesByTypeAnnexConfidentiality(self)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testAnnexes, prefix='test_subproduct_'))
    return suite
