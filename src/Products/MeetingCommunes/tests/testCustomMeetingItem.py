# -*- coding: utf-8 -*-
#
# File: testCustomMeetingItem.py
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

from DateTime import DateTime
from Products.MeetingCommunes.tests.MeetingCommunesTestCase import MeetingCommunesTestCase


class testCustomMeetingItem(MeetingCommunesTestCase):
    """
        Tests the MeetingItem adapted methods
    """
    def test_GetEchevinsForProposingGroup(self):
        '''Check a meetingItem for developers group return an echevin (the Same group in our case)
           and a meetingItem for vendors return no echevin.'''
        # create an item for test
        self.changeUser('pmManager')
        meetingDate = DateTime('2008/06/12 08:00:00')
        self.create('Meeting', date=meetingDate)
        # create items
        self.changeUser('pmCreator1')
        i1 = self.create('MeetingItem')
        i1.setProposingGroup('vendors')
        # before present in meeting, certfiedSignatures must be empty
        res = i1.adapted().getEchevinsForProposingGroup()
        self.assertEquals(res, [])
        self.changeUser('pmCreator1')
        i2 = self.create('MeetingItem')
        i2.setProposingGroup('developers')
        # before present in meeting, certfiedSignatures must be empty
        res = i2.adapted().getEchevinsForProposingGroup()
        self.assertEquals(res, ['developers'])
        # disabled MeetingGroup are still taken into account
        self.changeUser('admin')
        self.do(self.tool.developers, 'deactivate')
        self.assertEquals(self.wfTool.getInfoFor(self.tool.developers, 'review_state'), 'inactive')
        # getMeetingGroups called by getEchevinsForProposingGroup is memoized
        self.cleanMemoize()
        self.assertEquals(i2.adapted().getEchevinsForProposingGroup(), ['developers'])

