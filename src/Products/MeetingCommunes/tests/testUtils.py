# -*- coding: utf-8 -*-
#
# File: testUtils.py
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

from AccessControl import Unauthorized
from plone.app.testing import login
from Products.ExternalMethod.ExternalMethod import manage_addExternalMethod
from Products.MeetingCommunes.config import *
from Products.MeetingCommunes.tests.MeetingCommunesTestCase import \
    MeetingCommunesTestCase


class testUtils(MeetingCommunesTestCase):
    """
        Tests the Extensions/utils methods.
    """

    def setUp(self):
        MeetingCommunesTestCase.setUp(self)
        #add the ExternalMethod export_meetinggroups in Zope
        manage_addExternalMethod(self.portal.aq_inner.aq_parent, 'export_meetinggroups', '', 'Products.MeetingCommunes.utils', 'export_meetinggroups')
        #add the ExternalMethod import_meetinggroups in Zope
        manage_addExternalMethod(self.portal.aq_inner.aq_parent, 'import_meetinggroups', '', 'Products.MeetingCommunes.utils', 'import_meetinggroups')

    def _exportMeetingGroups(self):
        return self.portal.export_meetinggroups()

    def _importMeetingGroups(self, dict):
        return self.portal.import_meetinggroups(dict=str(dict))

    def test_accessToMethods(self):
        """
          Check that only Managers can access the methods
        """
        self.assertRaises(Unauthorized, self._exportMeetingGroups)
        self.assertRaises(Unauthorized, self._importMeetingGroups, {})

    def test_exportMeetingGroups(self):
        """
          Check that calling this method returns the right content
        """
        login(self.portal, 'admin')
        expected = {'vendors': ('Vendors', '', 'Devil', "python: item.id == 'recurringagenda1'"), 'developers': ('Developers', '', 'Devel', 'python:False')}
        res = self._exportMeetingGroups()
        self.assertEquals(expected, res)

    def test_importMeetingGroups(self):
        """
          Check that calling this method creates the MeetingGroups if not exist
        """
        login(self.portal, 'admin')
        #if we pass a dict containing the existing groups, it does nothing but
        #returning that the groups already exist
        dict = self._exportMeetingGroups()
        expected = 'MeetingGroup vendors already exists\nMeetingGroup developers already exists'
        res = self._importMeetingGroups(dict)
        self.assertEquals(expected, res)
        #but it can also add a MeetingGroup if it does not exist
        dict['newGroup'] = ('New group title', 'New group description', 'NGAcronym', 'python:False')
        expected = 'MeetingGroup vendors already exists\nMeetingGroup newGroup added\nMeetingGroup developers already exists'
        res = self._importMeetingGroups(dict)
        self.assertEquals(expected, res)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testUtils))
    return suite
