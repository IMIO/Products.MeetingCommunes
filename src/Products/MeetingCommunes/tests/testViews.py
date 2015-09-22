# -*- coding: utf-8 -*-
#
# File: testViews.py
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
from Products.PloneMeeting.tests.testViews import testViews as pmtv


class testViews(MeetingCommunesTestCase, pmtv):
    ''' '''

    def test_subproduct_call_ItemTemplates(self):
        '''Run the test_pm_ItemTemplates from PloneMeeting.'''
        pmtv.test_pm_ItemTemplates(self)

    def test_subproduct_call_ItemTemplatesWithSubFolders(self):
        '''Run the test_pm_ItemTemplatesWithSubFolders from PloneMeeting.'''
        pmtv.test_pm_ItemTemplatesWithSubFolders(self)

    def test_subproduct_call_ItemTemplatesWithSubFoldersContainedInEmptyFolders(self):
        '''Run the test_pm_ItemTemplatesWithSubFoldersContainedInEmptyFolders from PloneMeeting.'''
        pmtv.test_pm_ItemTemplatesWithSubFoldersContainedInEmptyFolders(self)

    def test_subproduct_call_JSVariables(self):
        '''Run the test_pm_JSVariables from PloneMeeting.'''
        pmtv.test_pm_JSVariables(self)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testViews, prefix='test_subproduct_'))
    return suite