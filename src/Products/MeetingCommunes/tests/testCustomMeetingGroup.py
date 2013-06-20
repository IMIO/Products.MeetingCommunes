# -*- coding: utf-8 -*-
#
# File: testCustomMeetingGroup.py
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

from plone.app.testing import login
from Products.MeetingCommunes.tests.MeetingCommunesTestCase import \
    MeetingCommunesTestCase


class testCustomMeetingGroup(MeetingCommunesTestCase):
    '''Tests the MeetingGroup adapted methods.'''

    def testListEchevinServices(self):
        login(self.portal, 'admin')
        from Products.Archetypes.atapi import DisplayList
        les = DisplayList([('developers', u'Developers'), ('vendors', u'Vendors')])
        meetingGroups = self.tool.objectValues('MeetingGroup')
        self.assertEquals(meetingGroups[0].listEchevinServices(), les)
